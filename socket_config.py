from abc import ABC, abstractmethod
import socket


"""
The SocketConfiguration is a base class for all socket configurations.

The Socket should be extended with the configuration.

Example:
    socket = SocketFactory().create_socket()
    socket.add_configuration(ResuseAddressConfiguration())

Provides a framework to add configurations to a socket.

"""
class SocketConfiguration(ABC):
    @abstractmethod
    def configure(self, socket: socket.socket):
        pass


class ResuseAddressConfiguration(SocketConfiguration):
    """
    The ResuseAddressConfiguration is a configuration for a socket that allows the socket to reuse the address.
    """
    def configure(self, sock: socket.socket) -> None:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


