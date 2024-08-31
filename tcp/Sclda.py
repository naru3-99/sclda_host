# 2024/06/24
# auther:naru
# encoding=utf-8
from Server.ScldaServer import server_init, QUEUE
from Analyzer.pid import process_pid
from Analyzer.syscall import process_syscall
from lib.fs import (
    get_all_file_path_in,
    get_all_dir_names_in,
    rmrf,
    ensure_path_exists,
)

from CONST import INPUT_DIR, INPUT_PID_DIR, OUTPUT_DIR, PORT_NUMBER


def main():
    # 前のデータを削除する
    rmrf(INPUT_DIR)
    rmrf(OUTPUT_DIR)
    # 入出力パスを生成する
    ensure_path_exists(INPUT_DIR)
    ensure_path_exists(OUTPUT_DIR)
    # サーバの初期化
    server_init()
    # 前処理を実施
    # pickleファイルまでのパス
    # processed_pidpath_ls = []
    # processed_scdata_lsls = [[] for _ in range(PORT_NUMBER)]
    # dir_name_ls = [d for d in get_all_dir_names_in(INPUT_DIR) if d != "PID"]

    # while True:
    #     if not QUEUE.empty():
    #         rmrf(OUTPUT_DIR)
    #         ensure_path_exists(OUTPUT_DIR)
    #         process_pid(get_all_file_path_in(INPUT_PID_DIR))
    #         for d in get_all_dir_names_in(INPUT_DIR):
    #             if "PID" in d:
    #                 continue
    #             process_syscall(f"{INPUT_DIR}{d}/")
    #         return

    #     # pidの処理
    #     current_pidpath_ls = get_all_file_path_in(INPUT_PID_DIR)
    #     new_pidpath_ls = [
    #         cpath for cpath in current_pidpath_ls if (not cpath in processed_pidpath_ls)
    #     ]
    #     process_pid(new_pidpath_ls)
    #     processed_pidpath_ls = current_pidpath_ls

    #     # syscallの処理
    #     for i, d in enumerate(dir_name_ls):
    #         path_ls = [
    #             p
    #             for p in get_all_file_path_in(f"{INPUT_DIR}{d}/")
    #             if not p in processed_scdata_lsls[i]
    #         ]
    #         process_syscall(path_ls)
    #         processed_scdata_lsls[i] += path_ls


if __name__ == "__main__":
    main()
