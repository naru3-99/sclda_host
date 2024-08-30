from Analyzer.pid import process_pid
from Analyzer.syscall import process_syscall
from lib.fs import (
    get_all_dir_names_in,
    get_all_file_path_in,
    rmrf,
    ensure_path_exists,
)

from CONST import (
    INPUT_DIR,
    INPUT_PID_DIR,
    OUTPUT_DIR,
)


def main():
    rmrf(OUTPUT_DIR)
    ensure_path_exists(OUTPUT_DIR)
    process_pid(get_all_file_path_in(INPUT_PID_DIR))
    for d in get_all_dir_names_in(INPUT_DIR):
        if ("PID" in d):
            continue
        process_syscall(f"{INPUT_DIR}{d}/")


if __name__ == "__main__":
    main()
