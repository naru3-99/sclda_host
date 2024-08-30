from lib.fs import get_all_file_path_in, load_object_from_file
from CONST import DECODE

# for o in load_object_from_file("./input/0/0.pickle")[0:10]:
#     print(o)
#     print("")

# o:bytes = load_object_from_file("./input/0/0.pickle")[0]

# for c in o:
#     if c == 18:
#         print(c)

for p in get_all_file_path_in("./input/0/"):
    for o in load_object_from_file(p):
        if len(o) < 50:
            print(len(o),o)
