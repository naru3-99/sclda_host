from lib.fs import (
    load_object_from_file,
    save_str_to_file,
    load_str_from_file,
)
from CONST import (
    OUTPUT_DIR,
    SYSCALL_INFO_PATH,
    SCLDA_DELIMITER,
    SCLDA_EACH_DLMT,
)

INDEX_PID = 0
INDEX_TIME = 1
INDEX_SCID = 2

pid__clock_scid__dict = {}
# (str)syscall id -> (str)syscall nameの辞書を段取り
id_name_dict = {}
for row in load_str_from_file(SYSCALL_INFO_PATH).split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_name_dict[splited_row[1]] = splited_row[0]


def __process_syscall(pickle_path):
    for packet in load_object_from_file(pickle_path):
        for msg in [msg for msg in packet.split(SCLDA_EACH_DLMT) if len(msg) != 0]:
            element_ls = [
                e.decode("latin-1", errors="replace")
                for e in msg.split(SCLDA_DELIMITER)
                if len(e) != 0
            ]
            # リストはpid, clock, scDATA... で長さが3以上のはず
            if len(element_ls) < 3:
                continue

            pid = element_ls[INDEX_PID]
            if not pid.isdigit():
                continue

            if not (pid in pid__clock_scid__dict.keys()):
                pid__clock_scid__dict[pid] = {}

            clock = element_ls[INDEX_TIME]
            if not (clock in pid__clock_scid__dict[pid].keys()):
                pid__clock_scid__dict[pid][clock] = ""

            scid = element_ls[INDEX_SCID]
            if scid in id_name_dict.keys():
                scname = f"{scid}-{id_name_dict[scid]}"
            else:
                scname = f"{scid}"

            other = "\t".join([e for e in element_ls[INDEX_SCID + 1 :]])
            pid__clock_scid__dict[pid][clock] += f"{scname}\t{other}"


def process_syscall(new_path_ls):
    for path in new_path_ls:
        __process_syscall(path)

    for pid in pid__clock_scid__dict.keys():
        path = f"{OUTPUT_DIR}{pid}.csv"
        msg_list = [
            f"{clock}\t{msg}" for clock, msg in pid__clock_scid__dict[pid].items()
        ]
        save_str_to_file("\n".join(msg_list), path)
