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
    SCLDA_DELIMITER,
    SCLDA_EACH_DLMT
)

# (str)syscall id -> (str)syscall nameの辞書を段取り
id_name_dict = {}
for row in load_str_from_file(SYSCALL_INFO_PATH).split("\n"):
    splited_row = row.split(",")
    if len(splited_row) == 0:
        continue
    id_name_dict[splited_row[1]] = splited_row[0]


def main():
    for e in load_object_from_file('./0.pickle'):
        for ee in [ee for ee in e.split(SCLDA_EACH_DLMT) if len(ee)!=0]:
            print([eee for eee in ee.split(SCLDA_DELIMITER) if len(eee)!=0])
        return


if __name__ == '__main__':
    main()