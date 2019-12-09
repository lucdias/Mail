import socket
import time

class Client:
	serverName = None
	serverPort = 7777
	dnsPort = 12000
	dnsIP = "192.168.0.108"
	serverAddress = None
	dnsAddress = (dnsIP, dnsPort)
	def __init__(self, sock = None):
	    if sock is None:
	        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	        self.setServerAddress()
	        self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	    else:
	    	self.sock = sock
	
	
	def setServerAddress(self):
		self.serverAddress = (self.getServerIP(), self.getServerPort())

	
	def getServerAddress(self):
		return self.serverAddress


	def connectClient(self, serverName):
		if self.serverName == None:
			self.setServerIP(self.getFromDns(serverName))
			self.setServerAddress()
			print(self.serverAddress)
		self.sock.connect(self.serverAddress)
	
	
	def disconnectClient(self):
		self.sendMessage("IOB")
		
	
	def createPackets(self, msg):
		if len(msg) > 2048:
			return [msg[i:i+2048] for i in range(0, len(msg), 2048)]
		else:
			return [msg]


	def sendMessage(self, msg):
		message = self.createPackets(msg)
		for sendMsg in message:
			print(sendMsg)
			self.sock.send(bytes(sendMsg, encoding='utf8'))
	
	
	def recvMsg(self):
		msg = self.sock.recv(2048)
		return msg.decode("utf-8")

	
	def recvSub(self):
		msg = self.sock.recv(2048)
		print(msg)
		return msg
	
	
	def getFromDns(self, serverName):
		sendMsg = "WHO " + serverName
		print(sendMsg)
		self.sock2.sendto(bytes(sendMsg, encoding='utf8'), self.dnsAddress)
		(IP, addr) = self.sock2.recvfrom(2048)
		print(IP.decode())
		return IP.decode()
		
	
	def setServerIP(self, IP):
		self.serverName = IP
	
	
	def getServerIP(self):
		return self.serverName
		
		
	def getServerPort(self):
		return self.serverPort
