import multiprocessing as mp
import time

from UdpServer import UdpServer
from lib.multp import start_process
from lib.fs import save_object_to_file, count_files_in_directory, ensure_path_exists

COM_SAVE_PROC_STOP = "\x02STOP\x03"


class UdpServerSaveFile(UdpServer):
    def __init__(self, host, port, bufsize, timeout, save_buf):
        super().__init__(host, port, bufsize, timeout)
        # いくつのメッセージが貯まると保存するか
        self._save_buf = save_buf

        # 保存するパスを渡すためのキュー
        # AutoDAとやり取りするために使用
        self._path_q = mp.Queue()
        # パケットを保存したリストを渡すためのキュー
        # 保存プロセスとやり取りするために使用
        self._msg_q = mp.Queue()

    def change_save_dir(self, save_dir: str):
        ensure_path_exists(save_dir)
        self._path_q.put(save_dir)

    def main(self):
        # パケットを貯めるリスト
        msgs_ls = []
        # パケットを保存するディレクトリ
        while self._path_q.empty():
            time.sleep(1)
        save_dir = self._path_q.get()

        # 保存プロセスを起動
        start_process(save_proccess, self._msg_q)

        while True:
            try:
                # 次のイテレーションに移行する場合
                if not self._path_q.empty():
                    self._msg_q.put((save_dir, msgs_ls.copy()))
                    msgs_ls.clear()
                    save_dir = self._path_q.get()

                # パケットを取得し、バッファにぶち込む
                msg = self.receive_udp_packet()
                if msg is None:
                    continue
                msgs_ls.append(msg)
                # 保存するか判断し、保存する
                if len(msgs_ls) >= self._save_buf:
                    self._msg_q.put((save_dir, msgs_ls.copy()))
                    msgs_ls.clear()
            except KeyboardInterrupt:
                return
            except Exception as e:
                print(f"Error in server-save-file-main loop: {str(e)}")


def save_proccess(queue: mp.Queue) -> None:
    # 取得したパケットを、ピクルで保存するプロセス
    while True:
        # queueには、コマンドかパケットが入っているリストが格納される
        item = queue.get()

        # 終了コマンドだった場合
        if item == COM_SAVE_PROC_STOP:
            return

        # パケットを保存する
        save_dir, packet_ls = item
        count = count_files_in_directory(save_dir)
        save_object_to_file(packet_ls, f"{save_dir}{count}.pickle")


if __name__ == "__main__":
    # init servers
    from CONST import *

    syscall_server_ls = [
        UdpServerSaveFile(
            SERVER_HOST,
            SYSCALL_BASEPORT + i,
            SYSCALL_BUFSIZE,
            DEFAULT_SERVER_TIMEOUT,
            SYSCALL_SAVESIZE,
        )
        for i in range(PORT_NUMBER)
    ]
    pidppid_server = UdpServerSaveFile(
        SERVER_HOST,
        PIDPPID_PORT,
        PIDPPID_BUFSIZE,
        DEFAULT_SERVER_TIMEOUT,
        PIDPPID_SAVESIZE,
    )
    process_ls = []
    for s in syscall_server_ls:
        p = start_process(s.main)
        process_ls.append(s)
        time.sleep(0.5)
    process_ls.append(start_process(pidppid_server.main))

    for i, s in enumerate(syscall_server_ls):
        s.change_save_dir(f"./test/{i}/")
    pidppid_server.change_save_dir("./test/PID/")
