import time
import multiprocessing as mp

from Server.TCPServerSaveFile import TcpServerSaveFile
from CONST import (
    SERVER_HOST,
    SYSCALL_BASEPORT,
    SYSCALL_BUFSIZE,
    DEFAULT_SERVER_TIMEOUT,
    SYSCALL_SAVESIZE,
    PORT_NUMBER,
    PIDPPID_PORT,
    PIDPPID_BUFSIZE,
    PIDPPID_SAVESIZE,
    INPUT_DIR,
    TIME_TO_WAIT_INIT,
    INPUT_PID_DIR,
)

from lib.multp import start_process

QUEUE = mp.Queue()

def server_init():
    # start pidppid server
    process_ls = []
    pidppid_server = TcpServerSaveFile(
        SERVER_HOST,
        PIDPPID_PORT,
        PIDPPID_BUFSIZE,
        DEFAULT_SERVER_TIMEOUT,
        PIDPPID_SAVESIZE,
        INPUT_PID_DIR,
        QUEUE,
    )
    process_ls.append(start_process(pidppid_server.main))
    time.sleep(TIME_TO_WAIT_INIT)

    # start syscall server
    syscall_server_ls = [
        TcpServerSaveFile(
            SERVER_HOST,
            SYSCALL_BASEPORT + i,
            SYSCALL_BUFSIZE,
            DEFAULT_SERVER_TIMEOUT,
            SYSCALL_SAVESIZE,
            f'{INPUT_DIR}{i}/',
            QUEUE
        )
        for i in range(PORT_NUMBER)
    ]
    for server in syscall_server_ls:
        process_ls.append(start_process(server.main))
        time.sleep(TIME_TO_WAIT_INIT)

    return process_ls
