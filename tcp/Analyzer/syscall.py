import re

from lib.fs import (
    load_object_from_file,
    load_str_from_file,
    save_str_to_file,
    append_str_to_file,
    is_exists,
)

from CONST import (
    DECODE,
    SYSCALL_INFO_PATH,
    OUTPUT_DIR,
    SCLDA_MSG_START,
    SCLDA_MSG_END,
    SCLDA_DELIMITER,
    PORT_NUMBER,
)


# (str)syscall id -> (str)syscall nameの辞書を段取り
id_name_dict = {}
for row in load_str_from_file(SYSCALL_INFO_PATH).split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_name_dict[splited_row[1]] = splited_row[0]

# 保存するデータを記録するための辞書
pid_scid_data_dict = {}


def contains_control_characters(byte_data):
    # 制御文字の範囲: 0-31, 127
    return any(0 <= byte <= 31 or byte == 127 for byte in byte_data)


def escape_control_characters(byte_data):
    # 制御文字をエスケープシーケンスに置き換える
    escaped_bytes = re.sub(
        rb"[\x00-\x1F\x7F]",
        lambda match: b"\\x" + f"{match.group(0)[0]:02x}".encode("ascii"),
        byte_data,
    )
    # バイト列を文字列に変換して返す
    return escaped_bytes.decode(DECODE, errors="replace")


def correct_rule1(s):
    corrected = []
    target_index_ls = []
    last_char = None
    for i, char in enumerate(s):
        if char == "s" or char == "e":
            if last_char == char:
                corrected.append("x")
                target_index_ls.append(i)
            else:
                last_char = char
                corrected.append(char)
        else:
            corrected.append(char)

    return "".join(corrected), target_index_ls


def correct_rule2(s):
    target_index = []
    corrected = []
    flag = False
    for i, char in enumerate(s):
        if char == "e":
            flag = True
        elif char == "s":
            flag = False

        if flag and char == "c":
            target_index.append(i)
            corrected.append("x")
        else:
            corrected.append(char)

    return "".join(corrected), target_index


def correct_rule3(s):
    target_index = []
    splited = ["s" + a for a in s.split("s") if (len(a) != 0)]
    i = 0
    for msg in splited:
        if msg.count("c") >= 3:
            i += len(msg)
            continue
        target_index.append(i)
        target_index.append(i + len(msg) - 1)
        i += len(msg)
    return target_index


def correct_rules(s):
    str1, id1 = correct_rule1(s)
    str2, id2 = correct_rule2(str1)
    id3 = correct_rule3(str2)
    return id1 + id2 + id3


# 断片化に対処するためのバッファ
sc_byte_str = [b"" for _ in range(PORT_NUMBER)]


def __process_sc(filepath: str, num: int):
    global sc_byte_str
    sc_byte_str[num] += b"".join(load_object_from_file(filepath))

    model_str = ""
    for char in sc_byte_str[num]:
        if char == SCLDA_MSG_START:
            model_str += "s"
        elif char == SCLDA_MSG_END:
            model_str += "e"
        elif char == SCLDA_DELIMITER:
            model_str += "c"
        else:
            model_str += "x"

    target_index_ls = correct_rules(model_str)

    temp_byte = []
    msg_ls = []
    msg_ls_ls = []

    for i, char in enumerate(sc_byte_str[num]):
        if i in target_index_ls:
            temp_byte.append(char)
            continue
        if char == SCLDA_MSG_START:
            temp_byte = []
            msg_ls = []
        elif char == SCLDA_MSG_END:
            if len(temp_byte) != 0:
                msg_ls.append(bytes(temp_byte))
                temp_byte = []
            if len(msg_ls) == 0:
                continue
            msg_ls_ls.append(msg_ls)
        elif char == SCLDA_DELIMITER:
            msg_ls.append(bytes(temp_byte))
            temp_byte = []
        else:
            temp_byte.append(char)

    # 断片化のせいでtemp_bstrやsplited_msg_lsが
    # 空でない場合、byte_strを次回に引き継ぐ
    splited_msg = b""
    if len(msg_ls) != 0:
        splited_msg += bytes([SCLDA_MSG_START]) + bytes([SCLDA_DELIMITER]).join(msg_ls)
    sc_byte_str[num] = splited_msg + bytes([SCLDA_DELIMITER]) + bytes(temp_byte)

    is_additional = False
    for msg_ls in msg_ls_ls:
        # scid, pid, time, scdataだから
        # 足りていない場合は廃棄する
        if len(msg_ls) < 4:
            # print(msg)
            continue

        scid, pid, time = [msg.decode(DECODE, errors="replace") for msg in msg_ls[0:3]]
        if not scid.isdigit() or (not pid.isdigit()) or (not time.isdigit()):
            continue

        scname = msg_ls[3]
        is_additional = True
        if contains_control_characters(scname):
            # additional information
            scname = escape_control_characters(scname)
        else:
            scname = scname.decode(DECODE, errors="replace")
            if scname.isdigit():
                is_additional = False

        other = ""
        if len(msg_ls) >= 5:
            for msg in msg_ls[4:]:
                if contains_control_characters(msg):
                    other += f"{escape_control_characters(msg)}\t"
                else:
                    encoded_msg = msg.decode(DECODE, errors="replace")
                    other += f"{encoded_msg}\t"

        if not pid in pid_scid_data_dict.keys():
            pid_scid_data_dict[pid] = {}

        if not scid in pid_scid_data_dict[pid].keys():
            pid_scid_data_dict[pid][scid] = ""

        # 二番目以降の情報のはず
        if is_additional:
            pid_scid_data_dict[pid][scid] += f"{scname}{other}"
            continue

        # 一番目の情報のはず
        scinfo = ""
        if scname in id_name_dict.keys():
            scinfo = f"{scname}-{id_name_dict[scname]}"
        else:
            scinfo = f"{scname}-unknown"
        pid_scid_data_dict[pid][scid] += f"{time}\t{scinfo}\t{other}\t"


def process_sc(new_path_ls: list, num: int):
    for path in new_path_ls:
        __process_sc(path, num)

    for pid in pid_scid_data_dict.keys():
        save_path = f"{OUTPUT_DIR}{pid}.csv"
        save_row_ls = []
        for scid in pid_scid_data_dict[pid].keys():
            save_row_ls.append(pid_scid_data_dict[pid][scid].replace("\n", "\\n"))

        if is_exists(save_path):
            append_str_to_file("\n".join(save_row_ls), save_path)
        else:
            save_str_to_file("\n".join(save_row_ls), save_path)
    pid_scid_data_dict.clear()
