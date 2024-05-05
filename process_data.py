from lib.fs import (
    load_object_from_file,
    save_str_to_file,
    load_str_from_file,
    get_all_file_path_in,
    get_all_dir_names_in,
    ensure_path_exists,
    rmrf,
)
from CONST import (
    OUTPUT_DIR,
    SYSCALL_INFO_PATH,
    SYSCALL_INPUTPATH,
    PID_INPUTPATH,
    INPUT_DIR,
)


def main():
    # 出力先のディレクトリを段取り
    ensure_path_exists(OUTPUT_DIR)

    # pickleになっているデータをcsvに
    process_pid_data()
    process_syscall_data()

    # 上記のシステムコール情報のcsvを、
    # 見やすくする+PIDごとにする
    split_syscall_by_pid()

    # pidの親子関係データを並べ替え
    sort_pid_list()


def process_pid_data():
    a = []
    for path in get_all_dir_names_in(INPUT_DIR):
        if path != "PID":
            continue
        for filepath in get_all_file_path_in(f"{INPUT_DIR}{path}/"):
            for msg in load_object_from_file(filepath):
                a.append(
                    "\t".join(
                        [str(s).strip("b'").strip("'") for s in msg.split(b"\x05")]
                    )
                )
    if "sclda\\x00" in a:
        a.remove("sclda\\x00")
    save_str_to_file("\n".join(a), PID_INPUTPATH)


def process_syscall_data():
    a = []
    for path in get_all_dir_names_in(INPUT_DIR):
        if path == "PID":
            continue
        for filepath in get_all_file_path_in(f"{INPUT_DIR}{path}/"):
            for msg in load_object_from_file(filepath):
                a.append(
                    "\t".join(
                        [str(s).strip("b'").strip("'") for s in msg.split(b"\x05")]
                    )
                )
    save_str_to_file("\n".join(a), SYSCALL_INPUTPATH)


def split_syscall_by_pid():
    # syscall id -> syscall nameの辞書を段取り
    id_name_dict = {}
    for row in load_str_from_file(SYSCALL_INFO_PATH).split("\n"):
        splited_row = row.split(",")
        if len(splited_row) == 0:
            continue
        id_name_dict[splited_row[1]] = splited_row[0]

    # pidとsched_clockが一致している部分を結合する
    edited_row_dict = {}
    for row in load_str_from_file(SYSCALL_INPUTPATH).split("\n"):
        splited_row = row.split("\t")
        pid = splited_row[0]
        clock = splited_row[1]
        if not pid in edited_row_dict.keys():
            edited_row_dict[pid] = {}
        if not clock in edited_row_dict[pid].keys():
            edited_row_dict[pid][clock] = []
        edited_row_dict[pid][clock].append("\t".join(splited_row[2:]))

    for pid in edited_row_dict.keys():
        save_row_dict = {}
        save_file_path = f"{OUTPUT_DIR}{pid}.csv"
        for clock in edited_row_dict[pid].keys():
            save_row_dict[int(clock)] = "".join(edited_row_dict[pid][clock])
        # ソートしてから保存する
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
        save_str_to_file("\n".join(save_row_ls), save_file_path)


def sort_pid_list():
    rows_splited_ls = [
        row.split("\t")
        for row in load_str_from_file(PID_INPUTPATH).split("\n")
        if (row != "sclda\\x00")
    ]
    sorted_rows = [
        "\t".join(row) for row in sorted(rows_splited_ls, key=lambda x: int(x[0]))
    ]
    save_str_to_file("\n".join(sorted_rows), f"{OUTPUT_DIR}sorted_pid.csv")


if __name__ == "__main__":
    main()
