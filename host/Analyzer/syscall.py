from lib.fs import (
    is_exists,
    load_object_from_file,
    save_str_to_file,
    append_str_to_file,
    load_str_from_file,
)
from CONST import (
    OUTPUT_DIR,
    SYSCALL_INFO_PATH,
)

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
                s.decode("latin-1", errors="replace") for s in msg.split(b"\x05")
            ]
            # pid,clock,scid,retval,...なはずなので、
            # 2未満の長さならパケット破棄
            if len(temp_ls) <= 2:
                continue
            pid = temp_ls[0]
            clock = temp_ls[1]
            if temp_ls[2] in id_name_dict.keys():
                scname = f"{temp_ls[2]}-{id_name_dict[temp_ls[2]]}"
            else:
                scname = ""
            other = "\t".join(temp_ls[2:]).replace("\n", "\\n")

            if not (pid in pid__clock_scid__dict.keys()):
                pid__clock_scid__dict[pid] = {}
            if not (clock in pid__clock_scid__dict[pid].keys()):
                pid__clock_scid__dict[pid][clock] = ""
            pid__clock_scid__dict[pid][clock] += scname + "\t" + other

    for pid in pid__clock_scid__dict.keys():
        save_file_path = f"{OUTPUT_DIR}{pid}.csv"
        save_row_ls = []
        for clock, msg in pid__clock_scid__dict[pid].items():
            save_row_ls.append(f"{clock}\t{msg}")
        if is_exists(save_file_path):
            append_str_to_file("\n".join(save_row_ls), save_file_path)
        else:
            save_str_to_file("\n".join(save_row_ls), save_file_path)
