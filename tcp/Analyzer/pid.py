from lib.fs import (
    is_exists,
    load_object_from_file,
    save_str_to_file,
    load_str_from_file,
)
from CONST import (
    PID_OUTPUT_PATH,
    HANDSHAKE,
)


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
            row = "\t".join(
                [s.decode("latin-1", errors="replace") for s in msg.split(b"\x05")]
            )
            new_info_ls.append(row)
    if HANDSHAKE in new_info_ls:
        new_info_ls.remove(HANDSHAKE)

    # 新しいPID情報を統合し、保存する
    tab_splited_pidls = [
        info.split("\t") for info in (current_pidls + new_info_ls) if (len(info) != 0)
    ]
    if len(tab_splited_pidls) == 0:
        return
    sorted_pid_ls = [
        "\t".join(row) for row in sorted(tab_splited_pidls, key=lambda x: int(x[0]))
    ]
    save_str_to_file("\n".join(sorted_pid_ls), PID_OUTPUT_PATH)
