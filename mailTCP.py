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
	

	def setUser(self, user):
		self.user = user
	

	def getUser(self):
		return self.user


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
