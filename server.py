import socket
import os
import constant
# protocolo de comunicação vai começar com SEND TO "nome" "msg"
# para receber vai ser GET FROM "nome"
#
#
		
os.system("bash folders.sh server")

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
	
	
	def checkMsg(self, msg):
		tempMsg = msg[0:constant.HEADERSIZE]
		command = tempMsg.split()
		if command[0] == "SEND":
			self.handleSend(command[2], command[1], msg[15:len(msg)])
		elif command[0] == "GET":
			self.handleGet(command[1])


	def handleSend(self, userTo, userFrom, msg):
		os.system(f"bash users.sh {userTo}")
		fMsg = open(f"SRmail/{userTo}/{userFrom}.txt", "w")
		fMsg.write(f"{userFrom}\n" + f"{msg}")
		fMsg.close()


	def handleGet(self, user):
		path = f"SRmail/{user}/"
		try:
			with os.scandir(path) as it:
				sum = 0
				for entry in it:
					sum += 1
					if entry.is_file():
						try:
							fMsg = open(path + entry.name, "r")
							self.sendMsg(fMsg.read())
							fMsg.close()
							#os.system(f"rm {path + entry.name}")
						except:
							print("erro ao enviar arquivo")
				if sum <= 0:
					self.sendMsg("zero emails")
		except FileNotFoundError:
			os.system(f"mkdir {path}")
			self.handleGet(user)
	
	
	def sendMsg(self, msg):
			self.sock.sendto(bytes(msg, encoding='utf8'), self.getClientAddress())
	
	
	def recvMsg(self):
		(messageRecv, clientAddress) = self.sock.recvfrom(2048)
		self.setClientAddress(clientAddress)
		print(f"Message from {self.getClientAddress()} have been received!:\n")
		self.checkMsg(messageRecv.decode("utf-8"))


serverSocket = Server()
while True:
    serverSocket.recvMsg()
