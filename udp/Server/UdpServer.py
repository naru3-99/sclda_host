import socket


class UdpServer:
    """
    A class representing a UDP server.

    Attributes:
        host (str): The host address to bind the server to.
        port (int): The port number to bind the server to.
        bufsize (int): The size of the buffer for receiving data.
        timeout (float): The timeout value for receiving data.

    Methods:
        receive_udp_packet: Receives a UDP packet from a client.

    """

    def __init__(self, host: str, port: int, bufsize: int, timeout: float):
        """
        Initializes a UdpServer instance.

        Args:
            host (str): The host address to bind the server to.
            port (int): The port number to bind the server to.
            bufsize (int): The size of the buffer for receiving data.
            timeout (float): The timeout value for receiving data.

        Raises:
            Exception: If there is an error creating the socket or binding the address.

        """
        self._address = (host, port)
        self._bufsize = bufsize
        self._timeout = timeout
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.bind(self._address)
        except Exception as e:
            raise e

    def receive_udp_packet(self):
        """
        Receives a UDP packet from a client.

        Returns:
            bytes: The received data as bytes.

        """
        try:
            self._sock.settimeout(self._timeout)
            rcv_data, _ = self._sock.recvfrom(self._bufsize)
            return rcv_data
        except:
            return None

    def close(self):
        """
        Closes the UDP socket.

        """
        try:
            self._sock.close()
        except Exception:
            return
