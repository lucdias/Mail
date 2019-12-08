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
		count = 0
		while count < 3 and statusConnection == "timeout":
			statusConnection = self.socket.connectClient("rafamail.com.br")
			count += 1
		if statusConnection == "IHB":
			statusConnection = self.sendLogin()
			count = 0
			while count < 3 and statusConnection == "timeout":
				statusConnection = self.sendLogin()
				count += 1
			if statusConnection == "ACK":
				return "Success"
			else:
				return "Server unavailable"
		else:
			return "Server unavailable"
	
			
	def sendLogin(self):
		self.socket.sendMessage(self.getUser())
		serverMsg = self.socket.recvMsg()
		return serverMsg
		
		
	def sendMail(self, destination, subject, body):
		self.socket.sendMessage(f"SEND///{destination}///" + f"{self.user}///" + f"{subject}///" + f"{body}")
		msg = self.socket.recvMsg()
		count = 0
		while msg == "timeout" and count < 3:
			self.socket.sendMessage(f"SEND///{destination}///" + f"{self.user}///" + f"{subject}///" + f"{body}")
			msg = self.socket.recvMsg()
			count += 1
		if msg == "timeout":
			return "Server unavailable"
		return msg
		
			
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
		count = 0
		while msg == "timeout" and count < 3:
			self.socket.sendMessage("box")
			msg = self.socket.recvSub()
			count += 1
		if msg == "timeout":
			return "Server unavailable"
		self.subjects = pickle.loads(msg)
		return "Sucess"
	
	
	def attMailTrash(self):
		self.socket.sendMessage("trash")
		msg = self.socket.recvSub()
		count = 0
		while msg == "timeout" and count < 3:
			self.socket.sendMessage("trash")
			msg = self.socket.recvSub()
			count += 1
		if msg == "timeout":
			return "Server unavailable"
		self.subjects = pickle.loads(msg)
		return "Sucess"
	
	
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
		count = 0
		while msg == "timeout" and count < 3:
			self.socket.sendMessage(f"GET///{index}")
			msg = self.socket.recvMsg()
			count += 1
		if msg == "timeout":
			return "Server unavailable"
		return msg
		
	
	def delFromId(self, index):
		self.socket.sendMessage(f"DEL///{index}")
		msg = self.socket.recvMsg()
		count = 0
		while msg == "timeout" and count < 3:
			self.socket.sendMessage(f"DEL///{index}")
			msg = self.socket.recvMsg()
			count += 1
		if msg == "timeout":
			return "Server unavailable"
		return msg
		
		
mail = Mail()
mail.setUser(input("Please put your user:\n"))
print(mail.connect())
while True:
	print("What do you want to do?\n1. Send Mail\n2. See Box\n3. See trash\n4. Exit\n")
	cmd = input()
	if cmd == '1':
		mail.sendMail(input("Please put your destination:\n"), input("Please put the subject:\n"), input("Please put the message:\n"))
	elif cmd == '2':
		mail.attMailBox()
		mail.displaySubs()
		index = input("What mail do you want to read?\n")
		print(mail.getBody(index))
		cmd = input("Do you want to delete the mail?\nY or N\n")
		if cmd == "Y":
			mail.delFromId(index)
	elif cmd == '3':
		mail.attMailTrash()
		mail.displaySubs()
		index = input("What mail do you want to read?\n")
		print(mail.getBody(index))
	elif cmd == '4':
		mail.disconnect()
		exit()
