import socket
import os
import constant
import handleMsg
# protocolo de comunicação vai começar com SEND TO "nome" "msg"
# para receber vai ser GET FROM "nome"
#
#
if constant.system == 'Linux':
	os.system("bash folders.sh server")
elif constant.system == 'Windows':
	os.system("folders.bat server")

class Server:
	serverPort = 7777
	clientAddress = None
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock.bind((socket.gethostname(), self.serverPort))
		else:
			self.sock = sock

	
	def setClientAddress(self, addr):
		self.clientAddress = addr
	
	
	def getClientAddress(self):
		return self.clientAddress
	
	
	def sendMsg(self, msg):
		self.sock.sendto(bytes(msg, encoding='utf8'), self.getClientAddress())
	
	
	def recvMsg(self):
		(messageRecv, clientAddress) = self.sock.recvfrom(2048)
		self.setClientAddress(clientAddress)
		print(f"Message from {self.getClientAddress()} have been received!:\n{messageRecv.decode('utf-8')} \n")
		return messageRecv.decode("utf-8")


serverSocket = Server()
while True:
    msg = serverSocket.recvMsg()
    msgtoSend = handleMsg.checkMsg(msg)
    print(msgtoSend)
    for it in msgtoSend:
    	serverSocket.sendMsg(it)
