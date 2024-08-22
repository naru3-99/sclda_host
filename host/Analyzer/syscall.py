from lib.fs import (
    load_object_from_file,
    save_str_to_file,
    load_str_from_file,
)
from CONST import (
    OUTPUT_DIR,
    SYSCALL_INFO_PATH,
    SCLDA_DELIMITER,
    SCLDA_EACH_DLMT
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


def process_one_pickle(pickle_path):
    packet_list = load_object_from_file(pickle_path)
    for packet in packet_list:
        syscall_msg_list = [syscall_msg for syscall_msg in packet.split(SCLDA_EACH_DLMT) if len(syscall_msg)!=0]
        for syscall_msg in syscall_msg_list:
            scmsg_element_list = [element.decode("latin-1", errors="replace") for element in syscall_msg.split(SCLDA_DELIMITER) if len(element) != 0]

            # リストはpid, clock, scDATA... で長さが3以上のはず
            if (len(scmsg_element_list) < 3):
                continue

            pid = scmsg_element_list[INDEX_PID]
            if (not pid.isdigit()):
                continue
            if not (pid in pid__clock_scid__dict.keys()):
                pid__clock_scid__dict[pid] = {}

            clock = scmsg_element_list[INDEX_TIME]
            if not (clock in pid__clock_scid__dict[pid].keys()):
                pid__clock_scid__dict[pid][clock] = ""

            scid = scmsg_element_list[INDEX_SCID]
            if scid in id_name_dict.keys():
                scname = f"{scid}-{id_name_dict[scid]}"
            else:
                scname = ""
            other = "\t".join(scmsg_element_list[INDEX_SCID:]).replace("\n","\\n")
            pid__clock_scid__dict[pid][clock] += f"{scname}\t{other}"

def process_syscall(new_path_ls):
    for path in new_path_ls:
        process_one_pickle(path)

    for pid in pid__clock_scid__dict.keys():
        path = f"{OUTPUT_DIR}{pid}.csv"
        msg_list = [f"{clock}\t{msg}" for clock, msg in pid__clock_scid__dict[pid].items()]
        save_str_to_file("\n".join(msg_list),path)
