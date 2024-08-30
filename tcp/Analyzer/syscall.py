from lib.fs import (
    load_object_from_file,
    save_str_to_file,
    load_str_from_file,
    is_exists,
    append_str_to_file,
)
from CONST import (
    OUTPUT_DIR,
    SYSCALL_INFO_PATH,
    SCLDA_DELIMITER,
    SCLDA_EACH_DLMT,
    DECODE,
)

INDEX_SCID = 0
INDEX_PID = 1
INDEX_TIME = 2
INDEX_SCNAME = 3

# (str)syscall id -> (str)syscall nameの辞書を段取り
id_name_dict = {}
for row in load_str_from_file(SYSCALL_INFO_PATH).split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_name_dict[splited_row[1]] = splited_row[0]

pid_scid_data_dict = {}


def process_syscall(target_path_ls):
    byte_str = b""
    for path in target_path_ls:
        byte_str += b"".join(
            [o.replace(bytes([0]), b"") for o in load_object_from_file(path)]
        )

    scid_ls = []
    for msg in [msg for msg in byte_str.split(SCLDA_EACH_DLMT) if (len(msg) != 0)]:
        element_ls = [
            e.decode(DECODE, errors="replace")
            for e in msg.split(SCLDA_DELIMITER)
            if len(e) != 0
        ]
        # リストはscid, pid, clock, scDATA... で長さが4以上のはず
        if len(element_ls) < 4:
            continue

        scid = element_ls[INDEX_SCID]
        if not scid.isdigit():
            continue

        pid = element_ls[INDEX_PID]
        if not pid.isdigit():
            continue

        if not (pid in pid_scid_data_dict.keys()):
            pid_scid_data_dict[pid] = {}

        if not (scid in pid_scid_data_dict[pid].keys()):
            pid_scid_data_dict[pid][scid] = ["", ""]

        clock = element_ls[INDEX_TIME]
        if not clock.isdigit():
            continue
        pid_scid_data_dict[pid][scid][0] = clock

        if scid in scid_ls:
            pid_scid_data_dict[pid][scid][1] += "\t".join(element_ls[INDEX_SCNAME:])
            continue

        scid_ls.append(scid)
        other = "\t".join(element_ls[INDEX_SCNAME + 1 :])
        scname = element_ls[INDEX_SCNAME]
        if scname in id_name_dict.keys():
            scdata = f"{scname}-{id_name_dict[scname]}"
        else:
            scdata = scname
        pid_scid_data_dict[pid][scid][1] += f"{scdata}\t{other}\t"

    for pid in pid_scid_data_dict.keys():
        path = f"{OUTPUT_DIR}{pid}.csv"

        clock_msg_dict = {}
        for scid in pid_scid_data_dict[pid].keys():
            clock, msg = pid_scid_data_dict[pid][scid]
            clock_msg_dict[int(clock)] = msg

        msg_ls = []
        for clock in sorted(clock_msg_dict.keys()):
            msg_ls.append(f"{clock}\t{msg}")

        if is_exists(path):
            append_str_to_file("\n".join(msg_ls), path)
        else:
            save_str_to_file("\n".join(msg_ls), path)
