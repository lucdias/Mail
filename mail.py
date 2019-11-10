import constant
import os
import client

class Mail:

	user = None
	socket = client.Client()
	
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


	def connect(self):
		statusConnection = self.socket.connectClient("RMail")
		if statusConnection == "Connected":
			statusConnection = sendLogin()
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
		self.socket.sendMessage(user)
		serverMsg = self.socket.recvMsg()
		if serverMsg == "OK":
			return "User connected"
		elif serverMsg == "BSY":
			return "Server unavailable"
		else:
			return self.sendLogin()
		
		
	def sendMail(self, destination, subject, body):
		self.socket.sendMessage(f"SEND {user}" + f" {destination}" + f" {subject}" + " {body}")
			
			
	def disconnect(self):
		self.socket.disconnectClient()
	
	
	def eraseMail(self):
		raise NotImplementedError


mail = Mail()
mail.connect()
