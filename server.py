import socket
import os
import constant
import handleMsg
import handleFolder
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
	login = None
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock.bind((socket.gethostname(), self.serverPort))
			self.sock.settimeout(5.0)
		else:
			self.sock = sock

	def setConnection(self, clientAddress):
		self.setClientAddress(clientAddress)
		print(self.getClientAddress())
		self.sock.sendto(bytes("Ok Connection", encoding='utf8'), self.getClientAddress()) # Primeira mensagem do cliente, enviando um Ok de estabelecimento de conexao

	
	def setLogin(self, message=None):
		self.login = message


	def setClientAddress(self, addr=None):
		self.clientAddress = addr
	
	
	def getClientAddress(self):
		return self.clientAddress
	
	def getLogin(self):
		return self.login
	
	def sendMsg(self, msg, Addr = self.getClientAddress()):
		self.sock.sendto(bytes(msg, encoding='utf8'), self.getClientAddress())
	
	
	def recvMsg(self):
		clientFlag = False
		try:
			(messageRecv, clientAddress) = self.sock.recvfrom(2048)
			print(messageRecv.decode())
		except socket.timeout:
			print('Server Timeout - line 52')
			return []
		if self.clientAddress != None:
			if self.clientAddress != clientAddress: # Checar se o client reservado é o mesmo recebido da mensagem
				self.sock.sendto(bytes("BSY", encoding='utf8'), clientAddress)
				return []

			if self.login == None:
				if self.clientAddress == clientAddress:
					self.setLogin(messageRecv.decode('utf-8'))
					#os.system("mkdir SRmail" + constant.bars + self.getLogin())
					os.system(constant.folders + " SRmail" + constant.bars + self.getLogin())
					#if not os.path.exists("SRmail" + f"{constant.bars}" + self.getLogin() + "sub.txt"):
						
					fileNumber = handleFolder.countFiles("SRmail" + constant.bars + serverSocket.getLogin() + constant.bars)
					self.sendMsg("Num " + str(fileNumber))
					while not clientFlag:
						try:
							(messageRecv, clientAddress) = self.sock.recvfrom(2048)
							clientFlag = True
						except socket.timeout:
							print('Server Timeout - line 70')
							pass
					print("Ok Num receive")
					return []
				else:
					self.sock.sendto(bytes("BSY", encoding='utf8'), clientAddress)
					return []

		else:
			if messageRecv.decode("utf-8") == "IHB":
				self.setConnection(clientAddress)
				return []

		print(f"Message from {self.getClientAddress()} have been received!:\n{messageRecv.decode('utf-8')} \n")
		print(f"clientAddress = {self.clientAddress}\nlogin = {self.login}\n")
		return messageRecv.decode("utf-8")

	def sendDns(self):
		self.dnsAddress = input("Type the DNS IP adress: ")
		msg = "REG " + "rafamail.com.br"
		print(msg)
		self.sock.sendto(bytes(msg, encoding='utf8'), (self.dnsAddress,self.dnsPort))
		rmsg = serverSocket.recvMsg()
		cmd = rmsg.split()
		while cmd[0] != "OK":
			self.sock.sendto(bytes(msg, encoding='utf8'), (self.dnsAddress,self.dnsPort))
			rmsg = self.recvMsg()
			cmd = rmsg.split()

serverSocket = Server()
serverSocket.sendDns()
while True:
	msg = serverSocket.recvMsg()
	if msg != []:
		if msg == "IOB":
			serverSocket.setClientAddress()
			serverSocket.setLogin()
		else:
			path = "SRmail" + constant.bars + serverSocket.getLogin() + constant.bars
			fileNumber = handleFolder.countFiles(path)
			msgtoSend = handleMsg.checkMsg(msg)
			print(msgtoSend)

			if fileNumber <= 0:
				serverSocket.sendMsg(constant.noMail)
			else:
				fileMessage = []
				AckReceive = False
				with os.scandir(path) as it:
					for entry in it:
						if entry.is_file():
							fMsg = open(path + entry.name, "r")
							print(f"Arquivo {entry.name} enviado")
							fileMessage.append(fMsg.read())
							serverSocket.sendMsg(entry.name[:-4] + fileMessage[0])

							while not AckReceive:
								try:
									(ACK, clientAddress) = serverSocket.sock.recvfrom(2048)
									AckReceive = True
								except socket.timeout:
									print('Server timeout - line 132')
									pass
							fMsg.close()
							fileMessage.clear()
							AckReceive = False
'''					
			    msgtoSend = handleMsg.checkMsg(msg)
			    if msgtoSend != None:
				    for it in msgtoSend:
				    	serverSocket.sendMsg(it)
'''
