import multiprocessing as mp
import time

from CONST import FINISH_COMMAND
from Server.TCPServer import TcpServer

from lib.multp import start_process
from lib.fs import (
    save_object_to_file,
    count_files_in_directory,
    ensure_path_exists,
)


class TcpServerSaveFile(TcpServer):

    def __init__(
        self,
        host: str,
        port: int,
        bufsize: int,
        timeout: float,
        save_bufsize: int,
        save_dir: str,
        msg_queue: mp.Queue,
    ):
        super().__init__(host, port, bufsize, timeout)
        # bufsize to save packets
        self._save_bufsize = save_bufsize
        # directory to save pickles
        self._save_dir = save_dir
        ensure_path_exists(save_dir)
        # queue to communicate with parent process
        self.msg_queue = msg_queue

    def main(self):
        # buffer for packet
        packet_buf = []

        while not self.accept_connection():
            time.sleep(1)

        while True:
            try:
                if not self.msg_queue.empty():
                    # 終了条件を満たしたため、終了する
                    if len(packet_buf) != 0:
                        start_process(save_proccess, packet_buf.copy(), self._save_dir)
                    self.close()
                    return

                packet = self.receive_tcp_packet()
                if packet is None:
                    continue

                if FINISH_COMMAND in packet:
                    self.msg_queue.put(FINISH_COMMAND)
                    if len(packet_buf) != 0:
                        start_process(save_proccess, packet_buf.copy(), self._save_dir)
                    self.close()
                    return

                packet_buf.append(packet)
                if len(packet_buf) >= self._save_bufsize:
                    start_process(save_proccess, packet_buf.copy(), self._save_dir)
                    packet_buf.clear()

            except KeyboardInterrupt:
                self.close()
                return

            except:
                pass


def save_proccess(packet_buffer: list, save_dir: str) -> None:
    # パケットを保存する
    count = count_files_in_directory(save_dir)
    save_object_to_file(packet_buffer, f"{save_dir}{count}.pickle")