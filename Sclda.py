# 2024/06/24
# auther:naru
# encoding=utf-8
from Server.ScldaServer import server_init
from Analyzer.process_data import process_pid, process_syscall
from lib.fs import get_all_file_path_in, get_all_dir_names_in
from CONST import INPUT_DIR, INPUT_PID_DIR


def main():
    # サーバの初期化
    server_init()
    # 前処理を実施
    # pickleファイルまでのパス
    processed_pidpath_ls = []
    processed_scpath_ls = []

    while True:
        try:
            # pidの処理
            current_pidpath_ls = get_all_file_path_in(INPUT_PID_DIR)
            new_pidpath_ls = [
                cpath
                for cpath in current_pidpath_ls
                if (not cpath in processed_pidpath_ls)
            ]
            process_pid(new_pidpath_ls)
            processed_pidpath_ls = current_pidpath_ls

            # syscallの処理
            current_dir_ls = [
                dirname
                for dirname in get_all_dir_names_in(INPUT_DIR)
                if dirname != "PID"
            ]
            current_scpath_ls = []
            for dirname in current_dir_ls:
                current_scpath_ls += get_all_file_path_in(dirname)

            new_scpath_ls = [
                cpath
                for cpath in current_scpath_ls
                if (not cpath in processed_scpath_ls)
            ]
            process_syscall(new_scpath_ls)
            processed_scpath_ls = current_scpath_ls
        except:
            pass


if __name__ == "__main__":
    main()
