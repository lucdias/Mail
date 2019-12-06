import constant
import os
import client
import time
import pickle

class Mail:

	user = None
	socket = client.Client()
	qntMails = None
	mailsBody = {}
	subjects = []
	@staticmethod
	def putIntoMailBox(msg):	
		if msg != constant.noMail:
			tempMsg = msg.split()
			fMsg = open(f"{constant.path}/{tempMsg[0]}.txt", "w")
			fMsg.write(msg)
			fMsg.close()

	def setUser(self, user):
		self.user = user
	

	def getUser(self):
		return self.user


	@staticmethod
	def countMails():
		count = 0
		with os.scandir(constant.path) as it:
			for i in it:
				count += 1
		return count


	@staticmethod
	def readMailBox():
		with os.scandir(constant.path) as it:
			for entry in it:
				if entry.is_file():
					fMsg = open(constant.path + "/" + entry.name, "r")
					print(fMsg.read())
					print("\n")
					fMsg.close()

	#modularizar melhor essa parte
	def connect(self):
		statusConnection = self.socket.connectClient("rafamail.com.br")
		if statusConnection == "Connected":
			statusConnection = self.sendLogin()
			if statusConnection != "User connected":
				return "Error"
			else:
				return "Success"
		else:
			return "Server unavailable"
	
			
	def sendLogin(self):
		self.socket.sendMessage(self.getUser())
		serverMsg = self.socket.recvMsg()
		while serverMsg != "OK":
			serverMsg = self.socket.recvMsg()
		self.setQntMails("0")
		if serverMsg == "BSY":
			return "Server unavailable"
		else:
			return "User connected"
		
		
	def sendMail(self, destination, subject, body):
		self.socket.sendMessage(f"SEND///{destination}///" + f"{self.user}///" + f"{subject}///" + f"{body}")
			
			
	def disconnect(self):
		print("estou desconectando")
		self.socket.disconnectClient()
	
	
	def eraseMail(self):
		raise NotImplementedError


	def setQntMails(self, numMail):
		self.qntMails = numMail


	def getQuantMails(self):
		return self.qntMails


	def attMailBox(self):
		self.socket.sendMessage("box")
		msg = self.socket.recvSub()
		self.subjects = pickle.loads(msg)
		
	
	def retMailsFromInbox(self):
		listRet = []
		Id = 0
		with os.scandir(constant.path) as it:
			for entry in it:
				if entry.is_file():
					fMsg = open(constant.path + "/" + entry.name, "r")
					msg = fMsg.read()
					msg = msg.split(None, 2)
					auxTuple = (msg[0], msg[1], Id)
					self.putBodyWithId(Id, msg[2])
					Id += 1
					listRet.append(auxTuple)
					fMsg.close()
		return listRet
	
	
	def displaySubs(self):
		index = 0
		for msg in self.subjects:
			print(f"{index}: {msg[0]} {msg[1]}")	
			index += 1	
	
	
	def getBody(self, index):
		self.socket.sendMessage(f"GET///{index}")
		msg = self.socket.recvMsg()
		return msg
		
		
mail = Mail()
mail.setUser(input("Please put your user:\n"))
mail.connect()
while True:
	esc = input("1. send mail\n2. read box\n3. exit\n")
	if esc == '1':
		mail.sendMail(input("Insira o destino: "), input("Insira o assunto: "), input("Insira a mensagem: "))
	elif esc == '2':
		mail.attMailBox()
		mail.displaySubs()
		index = input("qual email deseja utilizar?")
		os.system("clear")
		print(mail.getBody(index))
	elif esc == '3':
		mail.disconnect()
		exit()
#mail.attMailBox()
#mail.retMailsFromInbox()
#print(mail.getBodyFromId(0))
#mail.disconnect()
