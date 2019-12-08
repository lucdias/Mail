import constant
import os
import clientTCP
import time
import pickle

class Mail:

	user = None
	socket = clientTCP.Client()
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
		self.socket.connectClient("rafamail.com.br")
		self.sendLogin()
	
			
	def sendLogin(self):
		self.socket.sendMessage(self.getUser())
		
		
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
		print(self.subjects)
	
	
	def attMailTrash(self):
		self.socket.sendMessage("trash")
		msg = self.socket.recvSub()
		self.subjects = pickle.loads(msg)
	
	
	def displaySubs(self):
		index = 0
		for msg in self.subjects:
			print(f"{index}: {msg[0]} {msg[1]}")
			index += 1	
	
	
	def getBody(self, index):
		self.socket.sendMessage(f"GET///{index}")
		msg = self.socket.recvMsg()
		return msg
		
	
	def delFromId(self, index):
		self.socket.sendMessage(f"DEL///{index}")
		
		
mail = Mail()
mail.setUser(input("Please put your user:\n"))
mail.connect()
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
