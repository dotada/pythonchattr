import socket
s = socket.socket()
print("Socket successfully created")
port = 666
s.bind(('', port))
print("socket bound to %s" %(port))
s.listen(5)
print("socket is listening")
        

def getdata(client):
    while True:
        data = client.recv(2048)
        if data == b'dc':
            client.close()
            break
        if data != b'':
            print(data)  
        
while True:
    client_socket, address = s.accept()
    print(f"Connection established from {address}")
    getdata(client_socket)

