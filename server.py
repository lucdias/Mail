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
	clientAddress = None
	login = None
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock.bind((socket.gethostname(), self.serverPort))

			# Mandar nome e endereço pro DNS

		else:
			self.sock = sock

	def setConnection(self, clientAddress):
		self.setClientAddress(clientAddress)
		self.sock.sendto(bytes("Ok Connection", encoding='utf8'), self.getClientAddress()) # Primeira mensagem do cliente, enviando um Ok de estabelecimento de conexao

	
	def setLogin(self, message=None):
		self.login = message


	def setClientAddress(self, addr=None):
		self.clientAddress = addr
	
	
	def getClientAddress(self):
		return self.clientAddress
	
	def getLogin(self):
		return self.login
	
	def sendMsg(self, msg):
		self.sock.sendto(bytes(msg, encoding='utf8'), self.getClientAddress())
	
	
	def recvMsg(self):
		(messageRecv, clientAddress) = self.sock.recvfrom(2048)
		if self.clientAddress != None:
			if self.clientAddress != clientAddress: # Checar se o client reservado é o mesmo recebido da mensagem
				self.sock.sendto(bytes("BSY", encoding='utf8'), clientAddress)
				return []

			if self.login == None:
				if self.clientAddress == clientAddress:
					self.setLogin(messageRecv.decode('utf-8'))
					os.system("mkdir SRmail" + constant.bars + self.getLogin())
					fileNumber = handleFolder.countFiles("SRmail" + constant.bars + serverSocket.getLogin() + constant.bars)
					self.sendMsg("Num " + str(fileNumber))
					(messageRecv, clientAddress) = self.sock.recvfrom(2048)
					while messageRecv != "Ok Num" and clientAddress != self.clientAddress:
						(messageRecv, clientAddress) = self.sock.recvfrom(2048)
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


serverSocket = Server()
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
				with os.scandir(path) as it:
					for entry in it:
						if entry.is_file():
							fMsg = open(path + entry.name, "r")
							print(f"Arquivo {entry.name} enviado")
							fileMessage.append(fMsg.read())
							serverSocket.sendMsg(entry.name[:-4] + fileMessage[0])
							(ACK, clientAddress) = serverSocket.sock.recvfrom(2048)

							while ACK != "Ok" and clientAddress != serverSocket.getClientAddress():
								serverSocket.sendMsg(fileMessage)
								(ACK, clientAddress) = serverSocket.sock.recvfrom(2048)

							fMsg.close()
							fileMessage.clear()
'''
			    msgtoSend = handleMsg.checkMsg(msg)
			    if msgtoSend != None:
				    for it in msgtoSend:
				    	serverSocket.sendMsg(it)
'''