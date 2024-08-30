import socket


class TcpServer:
    """
    A class representing a TCP server.

    Attributes:
        host (str): The host address to bind the server to.
        port (int): The port number to bind the server to.
        bufsize (int): The size of the buffer for receiving data.
        timeout (float): The timeout value for receiving data.

    Methods:
        accept_connection: Accepts a connection from a TCP client.
        receive_tcp_packet: Receives a TCP packet from the connected client.
        close_connection: Closes the connection with the client.
        close_server: Closes the TCP server socket.

    """

    def __init__(self, host: str, port: int, bufsize: int, timeout: float):
        """
        Initializes a TcpServer instance.

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
        self._server_socket = None
        self._client_socket = None
        try:
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_socket.bind(self._address)
            self._server_socket.listen(1)
        except Exception as e:
            raise e

    def accept_connection(self):
        """
        Accepts a connection from a TCP client.

        Returns:
            bool: True if a connection is successfully accepted, False otherwise.
        """
        try:
            self._server_socket.settimeout(self._timeout)
            self._client_socket, _ = self._server_socket.accept()
            return True
        except Exception:
            return False

    def receive_tcp_packet(self):
        """
        Receives a TCP packet from the connected client.

        Returns:
            bytes: The received data as bytes, or None if there is an error.

        """
        try:
            if self._client_socket is None:
                return None

            self._client_socket.settimeout(self._timeout)
            msg = self._client_socket.recv(self._bufsize)
            return msg if (len(msg) != 0) else None

        except Exception:
            return None

    def close_connection(self):
        """
        Closes the connection with the client.

        """
        try:
            if self._client_socket:
                self._client_socket.close()
                self._client_socket = None
        except Exception:
            return

    def close_server(self):
        """
        Closes the TCP server socket.

        """
        try:
            self._server_socket.close()
        except Exception:
            return
