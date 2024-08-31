def correct_rule1(s):
    corrected = []
    target_index_ls = []
    last_char = None
    for i, char in enumerate(s):
        if char == "s" or char == "e":
            if last_char == char:
                corrected.append("x")
                target_index_ls.append(i)
            else:
                last_char = char
                corrected.append(char)
        else:
            corrected.append(char)

    return "".join(corrected), target_index_ls


def correct_rule2(s):
    target_index = []
    corrected = []
    flag = False
    for i, char in enumerate(s):
        if char == "e":
            flag = True
        elif char == "s":
            flag = False

        if flag and char == "c":
            target_index.append(i)
            corrected.append("x")
        else:
            corrected.append(char)

    return "".join(corrected), target_index


def correct_rule3(s):
    target_index = []
    s_splited = ["s" + a for a in s.split("s") if (len(a) != 0)]
    print(s_splited)


def correct_rules(s):
    str1, id1 = correct_rule1(s)
    str2, id2 = correct_rule2(str1)
    correct_rule3(str2)
    return id1 + id2


# テストケース
msg1 = "scxxxcxxxxcxxxe"  # 正常
msg2 = "scxxxcxxxxe"  # 異常：cが足りない
msg3 = "scxxxcsxxxxcxxsxe"  # 異常：sが含まれている
correct_rules(msg1 + msg2 + msg3)
