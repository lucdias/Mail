import constant
import os
import client
import time

class Mail:

	user = None
	socket = client.Client()
	qntMails = None
	mailsBody = {}
	
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
			self.socket.sendMessage("Ok Num")
			if statusConnection != "User connected":
				return "Error"
			else:
				return "Success"
		else:
			return "Server unavailable"
	
			
	def sendLogin(self):
		self.socket.sendMessage(self.getUser())
		serverMsg = self.socket.recvMsg()
		self.setQntMails("0")
		if serverMsg == "BSY":
			return "Server unavailable"
		else:
			print(serverMsg)
			quantMail = serverMsg.split()
			self.setQntMails(int(quantMail[1]))
			return "User connected"
		
		
	def sendMail(self, destination, subject, body):
		self.socket.sendMessage(f"SEND {user}" + f" {destination}" + f" {subject}" + " {body}")
			
			
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
		self.socket.sendMessage(f"GET {self.user}")
		aux = self.getQuantMails()
		msg = self.socket.recvMsg()
		while aux > 0:
			self.putIntoMailBox(msg)
			msg = self.socket.recvMsg()
			aux -= 1

	
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
	
	
	def putBodyWithId(self, Id, msg):
		self.mailsBody[Id] = msg
	
	
	def getBodyFromId(self, Id):
		return self.mailsBody[Id]
		
		
mail = Mail()
mail.setUser("jose")
print(mail.connect())
mail.attMailBox()
mail.retMailsFromInbox()
print(mail.getBodyFromId(0))
mail.disconnect()
