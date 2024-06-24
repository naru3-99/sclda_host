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
    PID_OUTPUT_PATH,
    HANDSHAKE,
)

# syscall id -> syscall nameの辞書を段取り
id_name_dict = {}
for row in load_str_from_file(SYSCALL_INFO_PATH).split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_name_dict[splited_row[1]] = splited_row[0]


def process_pid(new_path_ls):
    # 現在のPIDリストを読み込む
    if is_exists(PID_OUTPUT_PATH):
        current_pidls = load_str_from_file(PID_OUTPUT_PATH).split("\n")
    else:
        current_pidls = []

    # 新しいPID情報のリストを作成
    new_info_ls = []
    for filepath in new_path_ls:
        for msg in load_object_from_file(filepath):
            new_info_ls.append(
                "\t".join([str(s).strip("b'").strip("'") for s in msg.split(b"\x05")])
            )
    if HANDSHAKE in new_info_ls:
        new_info_ls.remove(HANDSHAKE)

    # 新しいPID情報を統合し、保存する
    tab_splited_pidls = [info.split("\t") for info in (current_pidls + new_info_ls)]
    sorted_pid_ls = [
        "\t".join(row) for row in sorted(tab_splited_pidls, key=lambda x: int(x[0]))
    ]
    save_str_to_file("\n".join(sorted_pid_ls), PID_OUTPUT_PATH)


def process_syscall(new_path_ls):
    # 新しいパケットを読み込む
    new_info_ls = []
    for path in new_path_ls:
        for msg in load_object_from_file(path):
            new_info_ls.append(
                "\t".join([str(s).strip("b'").strip("'") for s in msg.split(b"\x05")])
            )

    # pidとsched_clockが一致している部分を結合する
    edited_row_dict = {}
    for row in new_info_ls:
        splited_row = row.split("\t")
        pid = splited_row[0]
        clock = splited_row[1]
        if not pid in edited_row_dict.keys():
            edited_row_dict[pid] = {}
        if not clock in edited_row_dict[pid].keys():
            edited_row_dict[pid][clock] = []
        edited_row_dict[pid][clock].append("\t".join(splited_row[2:]))

    # ソートしてから保存する
    for pid in edited_row_dict.keys():
        save_row_dict = {}
        save_file_path = f"{OUTPUT_DIR}{pid}.csv"
        for clock in edited_row_dict[pid].keys():
            save_row_dict[int(clock)] = "".join(edited_row_dict[pid][clock])
        save_row_ls = []
        clock_ls = [k for k in save_row_dict.keys()]
        clock_ls.sort()
        min_clock = clock_ls[0]
        for clock in clock_ls:
            try:
                temp_splited = save_row_dict[clock].split("\t")
                save_row_ls.append(
                    f"{clock-min_clock}\t{id_name_dict[temp_splited[3]]}\t"
                    + "\t".join(temp_splited[4:])
                )
            except:
                pass
        if is_exists(save_file_path):
            append_str_to_file("\n".join(save_row_ls), save_file_path)
        else:
            save_str_to_file("\n".join(save_row_ls), save_file_path)
