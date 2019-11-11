import constant
import os
import client
import time

class Mail:

	user = None
	socket = client.Client()
	qntMails = None

	@staticmethod
	def putIntoMailBox(msg):	
		if msg != constant.noMail:
			tempMsg = msg.split()
			fMsg = open(f"{constant.path}/{tempMsg[0]}.txt", "w")
			fMsg.write(msg)


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
		statusConnection = self.socket.connectClient("RMail")
		print(statusConnection)
		time.sleep(1)
		if statusConnection == "Connected":
			statusConnection = self.sendLogin()
			self.socket.sendMessage("Ok Num")
			if statusConnection != "User connected":
				return "Error"
			else:
				return "Success"
		else:
			return "Server unavailable"
	
	
	def getQuantMails(self):
		quantMails = self.socket.recvMsg()
		if quantMails > -1:
			return quantMails
		else:
			return "Error"	
	
			
	def sendLogin(self):
		self.socket.sendMessage(self.getUser())
		serverMsg = self.socket.recvMsg()
		self.setQntMails(0)
		if serverMsg == "BSY":
			return "Server unavailable"
		else:
			self.setQntMails(serverMsg)
			return "User connected"
		
		
	def sendMail(self, destination, subject, body):
		self.socket.sendMessage(f"SEND {user}" + f" {destination}" + f" {subject}" + " {body}")
			
			
	def disconnect(self):
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
		while msg != "END":
			print(msg)
			putIntoMailBox(msg)
			msg = self.socket.recvMsg()


mail = Mail()
mail.setUser("Rafael")
print(mail.connect())
time.sleep(1)
mail.attMailBox()
time.sleep(1)
mail.disconnect()