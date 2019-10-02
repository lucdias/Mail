import socket

class Server:
    serverPort = 7777
    def __init__(self, sock = None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((socket.gethostname(), self.serverPort))
        else:
            self.sock = sock
    

serverSocket = Server()
while True:
    (messageRecv, address) = serverSocket.sock.recvfrom(2048)
    print(f"Message from {address} have been received!:" + "\n" + messageRecv.decode("utf-8"))
