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
	dnsPort = 12000
	clientAddress = None
	dnsAddress = None
	def __init__(self, sock = None, dnsSock = None):
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

	def sendDns(self):
		self.dnsAddress = input("Type the DNS IP adress: ")
		msg = "REG " + socket.gethostname()
		print(msg)
		self.sock.sendto(bytes(msg, encoding='utf8'), (socket.gethostname(),self.dnsPort))
		rmsg = serverSocket.recvMsg()
		cmd = rmsg.split()
		while cmd[0] != "OK":
			serverSocket.sendDns()
			rmsg = serverSocket.recvMsg()
			cmd = rmsg.split()


serverSocket = Server()
serverSocket.sendDns()
while True:
    msg = serverSocket.recvMsg()
    msgtoSend = handleMsg.checkMsg(msg)
    print(msgtoSend)
    for it in msgtoSend:
    	serverSocket.sendMsg(it)   