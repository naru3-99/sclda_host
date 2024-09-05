from Analyzer.pid import process_pid
from Analyzer.syscall import process_sc
from lib.fs import (
    get_all_dir_names_in,
    get_all_file_path_in,
    rmrf,
    ensure_path_exists,
)
from lib.multp import start_process

from CONST import (
    INPUT_DIR,
    INPUT_PID_DIR,
    OUTPUT_DIR,
)


def last_analyze():
    rmrf(OUTPUT_DIR)
    ensure_path_exists(OUTPUT_DIR)

    dir_len = len(get_all_file_path_in(INPUT_PID_DIR))
    process_pid([f"{INPUT_PID_DIR}{p}.pickle" for p in range(dir_len)])

    process_ls = []
    for d in get_all_dir_names_in(INPUT_DIR):
        if "PID" in d:
            continue
        dir_len = len(get_all_file_path_in(f"{INPUT_DIR}{d}/"))
        arg_list = [f"{INPUT_DIR}{d}/{i}.pickle" for i in range(dir_len)]
        p = start_process(process_sc, arg_list, int(d))
        process_ls.append(p)

    return process_ls


if __name__ == "__main__":
    last_analyze()
