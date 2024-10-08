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


def correct_rules(s):
    str1, id1 = correct_rule1(s)
    _, id2 = correct_rule2(str1)
    return id1 + id2


# 断片化に対処するためのバッファ
sc_byte_str = [b"" for _ in range(PORT_NUMBER)]
# scidとcntを識別しdataを保持する辞書
scid_cnt_data_dict = {}
# 保存するデータを記録するための辞書
pid_scid_data_dict = {}


def __process_sc1(filepath: str, num: int):
    global sc_byte_str, scid_cnt_data_dict
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

    # scidごとにデータを集める
    for msg_ls in msg_ls_ls:
        if len(msg_ls) < 2:
            continue
        scid = msg_ls[0].decode(DECODE, errors="replace")
        cnt = msg_ls[1].decode(DECODE, errors="replace")
        if not (scid.isdigit() and cnt.isdigit()):
            continue
        cnt = int(cnt)
        if not (scid in scid_cnt_data_dict.keys()):
            scid_cnt_data_dict[scid] = {}
        scid_cnt_data_dict[scid][cnt] = msg_ls[2:]


def __process_sc2():
    global scid_cnt_data_dict, pid_scid_data_dict
    # 同一scidをcntごとに並び替え
    for scid, cnt_data_dict in scid_cnt_data_dict.items():
        data_temp = []
        for cnt in sorted(cnt_data_dict.keys()):
            data_temp += cnt_data_dict[cnt]

        data = []
        for d in data_temp:
            if contains_control_characters(d):
                data.append(escape_control_characters(d))
            else:
                data.append(d.decode(DECODE, errors="replace"))

        if len(data) < 3:
            continue
        pid, time, scname = data[0:3]
        other = "\t".join(data[3:])

        # error check
        if not pid.isdigit():
            print(pid, data)
            continue
        if scname in id_name_dict.keys():
            scname = f"{scname}-{id_name_dict[scname]}"

        # append data
        if not (pid in pid_scid_data_dict.keys()):
            pid_scid_data_dict[pid] = {}
        pid_scid_data_dict[pid][scid] = f"{time}\t{scname}\t{other}"


def process_sc(new_path_ls: list, num: int):
    global pid_scid_data_dict, scid_cnt_data_dict

    for path in new_path_ls:
        __process_sc1(path, num)

    for path in new_path_ls:
        __process_sc2()

    for pid in pid_scid_data_dict.keys():
        save_path = f"{OUTPUT_DIR}{pid}.csv"
        save_row_ls = []
        for scid in pid_scid_data_dict[pid].keys():
            save_row_ls.append(pid_scid_data_dict[pid][scid].replace("\n", "\\n"))

        if is_exists(save_path):
            append_str_to_file("\n".join(save_row_ls), save_path)
        else:
            save_str_to_file("\n".join(save_row_ls), save_path)
    scid_cnt_data_dict.clear()
    pid_scid_data_dict.clear()