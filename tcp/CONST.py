# ./Server setting

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
PIDPPID_BUFSIZE = 50
SYSCALL_BUFSIZE = 1460

# パケットを何個単位で保存するか
PIDPPID_SAVESIZE = 20
SYSCALL_SAVESIZE = 1000

# パケットを解釈するための制御文字
# splitting syscall data by this delimiter
SCLDA_DELIMITER = 7
# msg must start with this
SCLDA_MSG_START = 18
# msg must end with this
SCLDA_MSG_END = 20

# サーバがタイムアウトするまでの秒数
DEFAULT_SERVER_TIMEOUT = 10.0

# serverを開始するまでのラグ
TIME_TO_WAIT_INIT = 0.3

# exit command
FINISH_COMMAND = b"sclda_reboot"


# ./Analyzer settings

# 入力のパス
INPUT_DIR = "./input/"
INPUT_PID_DIR = f"{INPUT_DIR}PID/"

# decode format
DECODE = "ASCII"

# 出力するパス
OUTPUT_DIR = "./output/"
PID_OUTPUT_PATH = f"{OUTPUT_DIR}pid.csv"

# handshake command
HANDSHAKE = b"sclda"
SYSCALL_INFO_PATH = "./syscall_info.csv"

# sshするために必要な情報
SSH_USERNAME = "naru3"
SSH_HOST = "127.0.0.1"
SSH_PASSWORD = "1234567890"
SSH_KEY = None
SSH_PORT = 16763