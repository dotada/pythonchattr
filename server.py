import socket
import ssl
s = socket.socket()
print("Socket successfully created")
port = 666
s.bind(('', port))
print("socket bound to %s" %(port))
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE
ssl_context.load_cert_chain(certfile='server.crt', keyfile='server.key')
s = ssl_context.wrap_socket(s, server_side=True)
s.listen(5)
print("socket is listening")
client_sockets = []
client_socket, address = "", ""
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
        client = None

while True:
    try:
        client_socket, address = s.accept()
        print(f"Connection established from {address}")
        client_sockets.append(client_socket)
        getdata(client_socket)
    except ConnectionResetError:
        client_sockets.remove(client_socket)
