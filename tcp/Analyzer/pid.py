from lib.fs import (
    load_object_from_file,
    save_str_to_file,
)
from CONST import (
    PID_OUTPUT_PATH,
    SCLDA_EACH_DLMT,
    SCLDA_DELIMITER,
    HANDSHAKE,
)

# dict[pid] -> "ppid(\t)comm"
pid_info_dict = {}


def __process_pid(filepath):
    byte_str = b"".join(load_object_from_file(filepath))
    data_ls = [msg for msg in byte_str.split(SCLDA_EACH_DLMT) if (len(msg) != 0) and (msg != HANDSHAKE)]
    for data in data_ls:
        splited_data = [msg.decode("ASCII", errors="replace") for msg in data.split(SCLDA_DELIMITER)]
        if len(splited_data) != 3:
            continue
        pid, ppid, comm = splited_data
        if not pid.isdigit():
            continue
        if pid in pid_info_dict.keys():
            continue
        pid_info_dict[int(pid)] = f"{ppid}\t{comm}"


def process_pid(new_path_ls):
    for path in new_path_ls:
        __process_pid(path)

    pid_ls = list(pid_info_dict.keys())
    pid_ls.sort()

    saving_data_ls = [f"{pid}\t{pid_info_dict[pid]}" for pid in pid_ls]

    save_str_to_file("\n".join(saving_data_ls), f"{PID_OUTPUT_PATH}")
