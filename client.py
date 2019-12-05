import socket
import time

class Client:
	serverName = None
	serverPort = 7777
	dnsPort = 12000
	dnsIP = "172.22.39.144"
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
		print(serverMsg)
		if serverMsg == "BSY":
			return "Error to connect"
		else:
			return "Connected"
	
	
	def disconnectClient(self):
		self.sendMessage("IOB")
		'''serverMsg = self.socket.recvMsg()
		if serverMsg == "OK":
			return "User disconnected"
		else:
			self.disconnectClient()
		'''
	
	def createPackets(self, msg):
		if len(msg) > 2048:
			return [msg[i:i+2048] for i in range(0, len(msg), 2048)]
		else:
			return [msg]


	def sendMessage(self, msg):
		message = self.createPackets(msg)
		for sendMsg in message:
			print(msg)
			print(self.serverAddress)
			self.sock.sendto(bytes(sendMsg, encoding='utf8'), self.serverAddress)
	
	
	def recvMsg(self):
		count = 0
		try:
			(msg, addr) = self.sock.recvfrom(2048)
		except socket.timeout:
			print("meme")
		else:
			return msg.decode("utf-8")

	
	def getFromDns(self, serverName):
		sendMsg = "WHO " + serverName
		print(sendMsg)
		self.sock.sendto(bytes(sendMsg, encoding='utf8'), self.dnsAddress)
		IP = self.recvMsg()
		print(IP)
		return IP
		
	
	def timer(self):
		raise NotImplementedError
	
	
	def setServerIP(self, IP):
		self.serverName = IP
	
	
	def getServerIP(self):
		return self.serverName
		
		
	def getServerPort(self):
		return self.serverPort
