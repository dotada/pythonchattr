import socket
import threading
import sys
import ssl


def get_data():
    """
    Receives data from a socket connection and prints it to the console.

    Returns:
        None
    """
    try:
        while True:
            data = s.recv(2000)
            if data != b'':
                print(data)
            else:
                pass
    except ConnectionAbortedError:
        sys.exit(0)


def send_data():
    """
    Reads input from the standard input and sends it over a socket connection.

    This function continuously reads input from the standard input using `sys.stdin.readline()`
    and sends the data over a socket connection. It keeps running in an infinite loop until
    a `KeyboardInterrupt` is raised.

    Parameters:
        None

    Returns:
        None
    """
    try:
        while True:
            data = input()
            if data.strip() == 'dc':
                s.send(data.strip().encode())
                s.close()
                sys.exit(0)
            if len(data) <= 2000:
                s.send(data.encode())
                data = ""
            else:
                print("Message too long.")
    except ConnectionAbortedError:
        sys.exit(0)


s = socket.socket()
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.verify_mode = ssl.CERT_NONE
s = ssl_context.wrap_socket(s, server_hostname='127.0.0.1')
port = 666
s.connect(('127.0.0.1', port))

try:
    t1 = threading.Thread(target=get_data)
    t1.start()
    t2 = threading.Thread(target=send_data)
    t2.start()
    t1.join()
    t2.join()
except ConnectionAbortedError:
    sys.exit(0)
