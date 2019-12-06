import socket
import os
import constant
import handleMsg
# protocolo de comunicação vai começar com SEND TO "nome" "msg"
# para receber vai ser GET FROM "nome"
#
#
os.system(constant.folders + " server")

class Server:
	serverPort = 7777
	clientAddress = None
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((socket.gethostname(), self.serverPort))
			self.sock.listen(1) # Testar se funciona nessa posicao
		else:
			self.sock = sock

	
	def setClientAddress(self, addr):
		self.clientAddress = addr
	
	
	def getClientAddress(self):
		return self.clientAddress
	
	
	def sendMsg(self, msg, connectionSocket):
		connectionSocket.send(bytes(msg, encoding='utf8'))
	
	
	def recvMsg(self, connectionSocket, clientAddress):
		messageRecv = connectionSocket.recv(2048)
		if not messageRecv:
			return []

		self.setClientAddress(clientAddress)
		print(f"Message from {self.getClientAddress()} have been received!:\n{messageRecv.decode('utf-8')} \n")
		return messageRecv.decode("utf-8")


serverSocket = Server()
while True:
	connectionSocket, clientAddress = serverSocket.sock.accept()
	while True:
	    msg = serverSocket.recvMsg(connectionSocket, clientAddress)
	    if msg == []:
	    	break

	    msgtoSend = handleMsg.checkMsg(msg)
	    print(msgtoSend)
	    for it in msgtoSend:
	    	serverSocket.sendMsg(it, connectionSocket)
	connectionSocket.close()