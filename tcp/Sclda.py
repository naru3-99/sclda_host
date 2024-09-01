# 2024/06/24
# auther:naru
# encoding=utf-8
from Analyzer.pid import process_pid
from Analyzer.syscall import process_sc
from LastPreprocess import last_analyze
from Server.ScldaServer import server_init, QUEUE
from lib.fs import rmrf, ensure_path_exists, get_all_file_path_in, get_all_dir_names_in

from CONST import (
    INPUT_DIR,
    OUTPUT_DIR,
    INPUT_PID_DIR,
    PORT_NUMBER,
)

pid_passed_ls = []
sc_passed_ls = [[] for _ in range(PORT_NUMBER)]


def analyze():
    global pid_passed_ls, sc_passed_ls
    dir_len = len(get_all_file_path_in(INPUT_PID_DIR))
    pid_arg_ls = [
        path
        for path in [f"{INPUT_PID_DIR}{x}.pickle" for x in range(dir_len)]
        if not path in pid_passed_ls
    ]
    process_pid(pid_arg_ls)
    pid_passed_ls += pid_arg_ls

    for d in get_all_dir_names_in(INPUT_DIR):
        if "PID" in d:
            continue
        dir_len = len(get_all_file_path_in(f"{INPUT_DIR}{d}/"))
        sc_arg_list = [
            path
            for path in [f"{INPUT_DIR}{d}/{i}.pickle" for i in range(dir_len)]
            if not path in sc_passed_ls[int(d)]
        ]
        process_sc(sc_arg_list, int(d))
        sc_passed_ls[int(d)] += sc_arg_list


def main():
    # 前のデータを削除する
    rmrf(INPUT_DIR)
    rmrf(OUTPUT_DIR)

    # 入出力パスを生成する
    ensure_path_exists(INPUT_DIR)
    ensure_path_exists(OUTPUT_DIR)

    # サーバの初期化
    server_init()

    # 取得したデータの解釈を行う
    while(QUEUE.empty()):
        analyze()

    # 最後の処理を行う
    last_analyze()


if __name__ == "__main__":
    main()
