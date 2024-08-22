# for AutoSclda
# hostのアドレス
SERVER_HOST = "192.168.56.1"
# プロセス生成に関わる、PIDとPPIDのペアを取得するポート
PIDPPID_PORT = 15001
# システムコールに関係する情報を取得する
# BASEPORT + (プロセッサID % 4)をPORTとして使用する
SYSCALL_BASEPORT = 15002
PORT_NUMBER = 16
# パケットの大きさに関するバッファサイズ
# see sclda/linux_6.1_mod/include/net/sclda.h
PIDPPID_BUFSIZE = 80
SYSCALL_BUFSIZE = 1200
# パケットを何個単位で保存するか
PIDPPID_SAVESIZE = 50
SYSCALL_SAVESIZE = 1000
# パケットを解釈するための制御文字
# splitting syscall data by this delimiter
SCLDA_DELIMITER =  b"\x05"
# splitting each infomation by this
SCLDA_EACH_DLMT =  b"\x06"

# サーバがタイムアウトするまでの秒数
DEFAULT_SERVER_TIMEOUT = 60
# serverを開始するまでのラグ
TIME_TO_WAIT_INIT = 0.3

# process_data.py
# 入力のパス
HANDSHAKE = "sclda\x00"
INPUT_DIR = "./input/"
INPUT_PID_DIR = f"{INPUT_DIR}PID/"
SYSCALL_INFO_PATH = "./syscall_info.csv"

# 出力するパス
OUTPUT_DIR = "./output/"
PID_OUTPUT_PATH = f"{OUTPUT_DIR}pid.csv"

# sshするために必要な情報
SSH_USERNAME = "naru3"
SSH_HOST = "127.0.0.1"
SSH_PASSWORD = "1234567890"
SSH_KEY = None
SSH_PORT = 16763