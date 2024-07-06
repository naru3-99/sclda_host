from lib.fs import (
    is_exists,
    load_object_from_file,
    save_str_to_file,
    append_str_to_file,
    load_str_from_file,
    get_all_file_path_in,
    rmrf,
)
from CONST import (
    OUTPUT_DIR,
    SYSCALL_INFO_PATH,
)
from Analyzer.process_data import process_syscall_last

# (str)syscall id -> (str)syscall nameの辞書を段取り
id_name_dict = {}
for row in load_str_from_file(SYSCALL_INFO_PATH).split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_name_dict[splited_row[1]] = splited_row[0]


def process_syscall(new_path_ls):
    # 新しいパケットを読み込む
    pid__clock_scid__dict = {}
    for path in new_path_ls:
        for msg in load_object_from_file(path):
            temp_ls = [
                s.decode("ISO-8859-1", errors="replace") for s in msg.split(b"\x05")
            ]
            # pid,clock,scid,retval,...なはずなので、
            # 2未満の長さならパケット破棄
            if len(temp_ls) <= 2:
                continue
            pid = temp_ls[0]
            clock = temp_ls[1]
            if temp_ls[2] in id_name_dict.keys():
                if id_name_dict[temp_ls[2]] != "read":
                    continue
                scname = "\t" + id_name_dict[temp_ls[2]]
            else:
                continue
            other = "\t".join(temp_ls[2:]).replace("\n", "\\n")

            if not (pid in pid__clock_scid__dict.keys()):
                pid__clock_scid__dict[pid] = {}
            if not (clock in pid__clock_scid__dict[pid].keys()):
                pid__clock_scid__dict[pid][clock] = ""
            pid__clock_scid__dict[pid][clock] += scname + "\t" + other

    for pid in pid__clock_scid__dict.keys():
        save_file_path = f"{OUTPUT_DIR}{pid}.csv"

        clock_msg_ls = [
            [int(clock), msg] for clock, msg in pid__clock_scid__dict[pid].items()
        ]
        sorted_clock_msg_ls = sorted(clock_msg_ls, key=lambda x: x[0])
        min_clock = sorted_clock_msg_ls[0][0]

        save_row_ls = []
        for clock, msg in sorted_clock_msg_ls:
            save_row_ls.append(f"{clock-min_clock}\t{msg}")
        if is_exists(save_file_path):
            append_str_to_file("\n".join(save_row_ls), save_file_path)
        else:
            save_str_to_file("\n".join(save_row_ls), save_file_path)


def delete_data():
    for path in get_all_file_path_in("./output"):
        if path == "./output/pid.csv":
            continue
        rmrf(path)


if __name__ == "__main__":
    delete_data()
    process_syscall_last([p for p in get_all_file_path_in("./input/") if (not "PID" in p)])
