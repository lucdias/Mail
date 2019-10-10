import platform
import os
import socket

if platform.system() == 'Linux':
	os.system("bash folders.sh client")
elif platform.system() == 'Windows':
	os.system("folders.bat")

path = "Rmail/CaixaPostal"

class Client:
	message = []
	serverName = socket.gethostname()
	serverPort = 7777
	user = None
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
		#self.sendMessage("OK")
		if msg.decode("utf-8") != "zero emails":
			fMsg = open(f"{path}/vouDecidir.txt", "w")
			fMsg.write(msg.decode("utf-8"))


	def setUser(self, user):
		self.user = user
	

	def getUser(self):
		return self.user


def intro(getEmail):
	print("Who are you?")
	getEmail.setUser(input())
	getEmail.sendMessage(f"GET {getEmail.getUser()}")
	getEmail.recvMsg()
	with os.scandir(path) as it:
		count = 0
		for i in it:
			count += 1
		print(f"You have {count} emails")


def menu(client):
	print("\nTo go to mail Box press 1\nTo send a email press 2\n")
	command = input()
	if command == '1':
		with os.scandir(path) as it:
			for entry in it:
				if entry.is_file():
					fMsg = open(path + "/" + entry.name, "r")
					print(fMsg.read())
					print("\n")
					fMsg.close()
					#os.system(f"rm {path + entry.name}")
	elif command == '2':
		print("Put the destination and then the message")
		msg = f"SEND {client.getUser()} " + input()
		print(msg)
		client.sendMessage(msg)


clientSocket = Client()
intro(clientSocket)
while True:
	menu(clientSocket)
