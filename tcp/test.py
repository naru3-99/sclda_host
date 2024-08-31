from lib.fs import (
    load_object_from_file,
    save_str_to_file,
)
from CONST import (
    PID_OUTPUT_PATH,
    SCLDA_EACH_DLMT,
    SCLDA_DELIMITER,
    HANDSHAKE,
    DECODE,
)

# dict[pid] -> "ppid(\t)comm"
pid_info_dict = {}

byte_str = b""


def __process_pid(filepath):
    global byte_str
    byte_str += b"".join(load_object_from_file(filepath))
    temp_bstr = b""
    splited_msg_ls = []
    msg_lsls = []
    for c in byte_str:
        if c == 0:
            continue
        if c == SCLDA_EACH_DLMT:
            if (len(temp_bstr) != 0):
                splited_msg_ls.append(temp_bstr)
            if len(splited_msg_ls) == 0:
                continue
            msg_lsls.append(splited_msg_ls)
            splited_msg_ls = []
        elif c == SCLDA_DELIMITER:
            splited_msg_ls.append(temp_bstr)
            temp_bstr = b""
        else:
            temp_bstr += bytes([c])

    print(msg_lsls)
    return
    if temp_bstr == HANDSHAKE:
        temp_bstr = b""

    # 断片化のせいでtemp_bstrやsplited_msg_lsが
    # 空でない場合、byte_strを次回に引き継ぐ
    splited_msg = b""
    if len(splited_msg_ls) != 0:
        splited_msg += SCLDA_DELIMITER.join([splited_msg_ls])
    byte_str = splited_msg + temp_bstr

    for splited_msg_ls in msg_lsls:
        # 長さが3(pid, ppid, comm)以外は
        # エラーとみなし、廃棄する
        if len(splited_msg_ls) != 3:
            continue

        pid, ppid, comm = splited_msg_ls
        if not pid.isdigit():
            continue
        pid_info_dict[int(pid)] = f"{ppid}\t{comm}"


def process_pid(new_path_ls):
    for path in new_path_ls:
        # obj = load_object_from_file(path)
        # print(obj)
         __process_pid(path)

    # pid_ls = list(pid_info_dict.keys())
    # pid_ls.sort()

    # saving_data_ls = [f"{pid}\t{pid_info_dict[pid]}" for pid in pid_ls]
    # save_str_to_file("\n".join(saving_data_ls), f"{PID_OUTPUT_PATH}")

    # pid_info_dict.clear()

if __name__ == '__main__':
    obj = load_object_from_file('./input/PID/0.pickle')
    for c in obj[1]:
        print(bytes([c]),c)
