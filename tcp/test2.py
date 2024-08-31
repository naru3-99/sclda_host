import re


def escape_control_characters(byte_data):
    # 制御文字をエスケープシーケンスに置き換える
    escaped_bytes = re.sub(
        rb"[\x00-\x1F\x7F]",
        lambda match: b"\\x" + f"{match.group(0)[0]:02x}".encode("ascii"),
        byte_data,
    )
    # バイト列を文字列に変換して返す
    return escaped_bytes.decode("ascii")


# 使用例
byte_data = b"\x01Hello\x7fWorld\x02"
escaped_str = escape_control_characters(byte_data)
print(escaped_str)
