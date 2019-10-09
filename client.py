import platform
import os
import socket

if platform.system() == 'Linux':
	os.system("bash folders.sh client")
elif platform.system() == 'Windows':
	os.system("folders.bat")

class Client:
	message = []
	serverName = socket.gethostname()
	serverPort = 7777
	def __init__(self, sock = None):
	    if sock is None:
	        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	        self.setServerAddress()
	    else:
	    	self.sock = sock
	
	
	def setServerAddress(self):
		self.serverAddress = (self.serverName, self.serverPort)


	def getServerPort(self):
		return self.serverPort


	def connectClient(self, host, port):
		raise NotImplementedError

	
	def createPackets(self, msg):
		if len(msg) > 2048:
			return [msg[i:i+2048] for i in range(0, len(msg), 2048)]
		else:
			return [msg]


	def sendMessage(self, msg):
		self.message = self.createPackets(msg)
		for sendMsg in self.message:
			self.sock.sendto(bytes(sendMsg, encoding='utf8'), self.serverAddress)
	
	
	def recvMsg(self):
		(msg, addr) = self.sock.recvfrom(2048)
		fMsg = open("Rmail/CaixaPostal/vouDecidir.txt", "w")
		fMsg.write(msg.decode("utf-8"))
			
			
clientSocket = Client()
print("Send message to the server: ")
while True:
	msg = input()
	clientSocket.sendMessage(msg)
	verify = msg.split()
	if verify[0] == "GET":
		clientSocket.recvMsg()
