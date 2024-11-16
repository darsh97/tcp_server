from typing import List
import socket
from socket_config import SocketConfiguration

"""
The SocketFactory is a factory for creating sockets with configurations.
"""

class SocketFactory:
    def __init__(self):
        self._configurations: List[SocketConfiguration] = []


    def add_configuration(self, configuration: SocketConfiguration) -> None:
        """ 
        Adds a configuration to the socket factory.
        """
        self._configurations.append(configuration)

        # Return self to allow for method chaining
        return self
    

    def create_socket(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print("Applying Configuration to Socket")
        for config in self._configurations:
            try:
                config.configure(sock)
                print(f"Applied configuration: {config.__class__.__name__}")
            except Exception as e:
                print(f"Failed to apply configuration {config.__class__.__name__}: {e}")
                raise
        return sock