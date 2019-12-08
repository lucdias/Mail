import socket
import time

class Client:
	serverName = None
	serverPort = 7777
	dnsPort = 12000
	dnsIP = "192.168.0.13"
	serverAddress = None
	dnsAddress = (dnsIP, dnsPort)
	def __init__(self, sock = None):
	    if sock is None:
	        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	        self.sock.settimeout(0.5)
	        self.setServerAddress()
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
		self.sendMessage("IHB")
		serverMsg = self.recvMsg()
		return serverMsg	
	
	
	def disconnectClient(self):
		self.sendMessage("IOB")
		serverMsg = self.recvMsg()
		count = 0
		while serverMsg != "IOB" and count < 3:
			self.sendMessage("IOB")
			serverMsg = self.recvMsg()
			count += 1
		return "User desconnected"
		
	
	def createPackets(self, msg):
		if len(msg) > 2048:
			return [msg[i:i+2048] for i in range(0, len(msg), 2048)]
		else:
			return [msg]


	def sendMessage(self, msg):
		message = self.createPackets(msg)
		print(self.serverAddress)
		for sendMsg in message:
			self.sock.sendto(bytes(sendMsg, encoding='utf8'), ('192.168.0.13', 7777))
	
	
	def recvMsg(self):
		count = 0
		try:
			(msg, addr) = self.sock.recvfrom(2048)
		except socket.timeout:
			return "timeout"
		else:
			return msg.decode("utf-8")

	
	def recvSub(self):
		count = 0
		try:
			(msg, addr) = self.sock.recvfrom(2048)
		except socket.timeout:
			return "timeout"
		else:
			return msg
	
	
	def getFromDns(self, serverName):
		sendMsg = "WHO " + serverName
		print(sendMsg)
		self.sock.sendto(bytes(sendMsg, encoding='utf8'), self.dnsAddress)
		IP = self.recvMsg()
		print(IP)
		return IP
		
	
	def setServerIP(self, IP):
		self.serverName = IP
	
	
	def getServerIP(self):
		return self.serverName
		
		
	def getServerPort(self):
		return self.serverPort
