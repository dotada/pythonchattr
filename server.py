# pylint: disable=missing-module-docstring, invalid-name, consider-using-f-string, line-too-long
import socket
import ssl
import threading
s = socket.socket()
print("Socket successfully created")
port = 666
s.bind(('', port))
print("socket bound to %s" % (port))
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.load_cert_chain(certfile='fullchain.pem', keyfile='privkey.pem')
s = ssl_context.wrap_socket(s, server_side=True)
s.listen(5)
print("socket is listening")
client_sockets = []


def getdata(client):
    """
    Receive data from a client and print it until a termination signal is received.

    Parameters:
        client (socket): The client socket to receive data from.

    Raises:
        ConnectionResetError: If the client connection is reset.

    Returns:
        None
    """
    try:
        while True:
            data = client.recv(2048)
            if data == b'dc':
                client.close()
                client_sockets.remove(client)
                break
            if data != b'':
                print(data)
                for cliente in client_sockets:
                    cliente.send(data)
    except ConnectionResetError:
        client_sockets.remove(client)
        client = None


def connection():
    """
    Establishes a connection with a client socket and starts a new thread to handle the client's data.

    Parameters:
        None

    Returns:
        None
    """
    client_socket = ""
    while True:
        try:
            client_socket, address = s.accept()
            print(f"Connection established from {address}")
            client_sockets.append(client_socket)
            client_thread = threading.Thread(
                target=getdata, args=(client_socket,))
            client_thread.start()
        except ConnectionResetError:
            client_sockets.remove(client_socket)
            client_socket = None


accept_thread = threading.Thread(target=connection)
accept_thread.start()
