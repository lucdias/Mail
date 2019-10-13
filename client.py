import platform
import os
import socket

class Client:
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

	
	def getServerAddress(self):
		return self.serverAddress


	def connectClient(self, host, port):
		raise NotImplementedError

	
	def createPackets(self, msg):
		if len(msg) > 2048:
			return [msg[i:i+2048] for i in range(0, len(msg), 2048)]
		else:
			return [msg]


	def sendMessage(self, msg):
		message = self.createPackets(msg)
		for sendMsg in message:
			self.sock.sendto(bytes(sendMsg, encoding='utf8'), self.serverAddress)
	
	
	def recvMsg(self):
		(msg, addr) = self.sock.recvfrom(2048)
		return msg.decode("utf-8")
		
