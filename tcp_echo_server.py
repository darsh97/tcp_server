'''
simple Synchronous TCP Echo Server.

1) Create a socket
2) Bind the socket to an address
3) Listen for connections
4) Accept a connection
5) Send/Receive data
6) Close the connection

'''
import socket
from contextlib import contextmanager
from socket_factory import SocketFactory
from socket_config import ResuseAddressConfiguration


# Constants
HOST = 'localhost'
PORT = 8080
ALLOWED_CONNECTIONS = 2

@contextmanager
def create_server_socket(socket_factory: SocketFactory):
    print("Socket for server being created\n")
    server_socket = socket_factory.create_socket()
    try:
        yield server_socket
    finally:
        server_socket.close()

@contextmanager
def manage_client_connection(client_socket):
    try:
        yield client_socket
    finally:
        client_socket.close()

def handle_client(client_socket, address):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print(f'Client {address} disconnected')
                break
            else:
                print(f'Echoing data from {address}: {data.decode()}')
                # Send the data back to the client
                client_socket.sendall(data)
        except KeyboardInterrupt:
            print(f"\nClosing connection to {address}")
            break
        except Exception as e:
            print(f"Socket Error with {address}: {e}")
            break

def server():
    socket_factory = SocketFactory()
    socket_factory.add_configuration(ResuseAddressConfiguration())
    with create_server_socket(socket_factory) as server_socket:
        print("Server Socket Created")
        server_socket.bind((HOST, PORT))
        print(f"Server Socket Bound to Address {HOST}:{PORT}")
        server_socket.listen(ALLOWED_CONNECTIONS)
        print("Server Listening")
        print(f'Server is running on {HOST}:{PORT}')

        while True:
            try:
                client_connection, address = server_socket.accept()
                handle_client(client_connection, address)
            except KeyboardInterrupt:
                print("\nShutting down server...")
                break
            except Exception as e:
                print(f"Error accepting connection: {e}")
                continue  # Continue accepting other connections

if __name__ == "__main__":
    server()
