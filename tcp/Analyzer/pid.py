from lib.fs import (
    load_object_from_file,
    save_str_to_file,
    append_str_to_file,
    is_exists,
)
from CONST import (
    SCLDA_MSG_START,
    SCLDA_MSG_END,
    SCLDA_DELIMITER,
    PID_OUTPUT_PATH,
    DECODE,
)

# dict[pid] -> "ppid(\t)comm"
pid_info_dict = {}
pid_byte_str = b""


def __process_pid(filepath):
    global pid_byte_str
    pid_byte_str += b"".join(load_object_from_file(filepath))

    temp_bstr = b""
    msg_ls = []
    msg_ls_ls = []
    for c in pid_byte_str:
        if c == 0:
            continue
        if c == SCLDA_MSG_START:
            temp_bstr = b""
            msg_ls = []
        elif c == SCLDA_MSG_END:
            if len(temp_bstr) != 0:
                msg_ls.append(temp_bstr)
            if len(msg_ls) == 0:
                continue
            msg_ls_ls.append(msg_ls)
        elif c == SCLDA_DELIMITER:
            msg_ls.append(temp_bstr)
            temp_bstr = b""
        else:
            temp_bstr += bytes([c])

    # 断片化のせいでtemp_bstrやsplited_msg_lsが
    # 空でない場合、byte_strを次回に引き継ぐ
    splited_msg = b""
    if len(msg_ls) != 0:
        splited_msg += bytes([SCLDA_MSG_START]) + bytes([SCLDA_DELIMITER]).join(msg_ls)
    pid_byte_str = splited_msg + bytes([SCLDA_DELIMITER]) + temp_bstr

    for msg_ls in msg_ls_ls:
        # 長さが3(pid, ppid, comm)以外は
        # エラーとみなし、廃棄する
        if len(msg_ls) != 3:
            continue

        pid, ppid, comm = [msg.decode(DECODE) for msg in msg_ls]
        if not pid.isdigit():
            continue
        pid_info_dict[int(pid)] = f"{ppid}\t{comm}"


def process_pid(new_path_ls):
    for path in new_path_ls:
        __process_pid(path)

    saving_data_ls = [
        f"{pid}\t{pid_info_dict[pid]}" for pid in sorted(list(pid_info_dict.keys()))
    ]
    if is_exists(PID_OUTPUT_PATH):
        append_str_to_file("\n".join(saving_data_ls), PID_OUTPUT_PATH)
    else:
        save_str_to_file("\n".join(saving_data_ls), PID_OUTPUT_PATH)
    pid_info_dict.clear()
