import constant
import os
import client
import time
import pickle

class Mail:

	user = None
	socket = client.Client()
	mailsBody = {}
	subjects = []
	

	def setUser(self, user):
		self.user = user
	

	def getUser(self):
		return self.user


	#modularizar melhor essa parte
	def connect(self, server):
		statusConnection = self.socket.connectClient(server)
		count = 0
		while count < 10 and statusConnection == "timeout":
			statusConnection = self.socket.connectClient(server)
			count += 1
		if statusConnection == "IHB":
			statusConnection = self.sendLogin()
			count = 0
			while count < 10 and statusConnection == "timeout":
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
		while msg == "timeout" and count < 10:
			self.socket.sendMessage(f"SEND///{destination}///" + f"{self.user}///" + f"{subject}///" + f"{body}")
			msg = self.socket.recvMsg()
			count += 1
		if msg == "timeout":
			return "Server unavailable"
		return msg
		
			
	def disconnect(self):
		print("estou desconectando")
		self.socket.disconnectClient()


	def attMailBox(self):
		self.socket.sendMessage("box")
		msg = self.socket.recvSub()
		count = 0
		while msg == "timeout" and count < 10:
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
		while msg == "timeout" and count < 10:
			self.socket.sendMessage("trash")
			msg = self.socket.recvSub()
			count += 1
		if msg == "timeout":
			return "Server unavailable"
		self.subjects = pickle.loads(msg)
		return "Sucess"
	
	
	def displaySubs(self):
		index = 0
		for msg in self.subjects:
			print(f"{index}: {msg[0]} {msg[1]}")
			index += 1	
	
	
	def getBody(self, index):
		self.socket.sendMessage(f"GET///{index}")
		msg = self.socket.recvMsg()
		count = 0
		while msg == "timeout" and count < 10:
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
		while msg == "timeout" and count < 10:
			self.socket.sendMessage(f"DEL///{index}")
			msg = self.socket.recvMsg()
			count += 1
		if msg == "timeout":
			return "Server unavailable"
		return msg
		
		
mail = Mail()

server = input("What server do you want to connect?\n")
mail.setUser(input("Please put your user:\n"))

if mail.connect(server) ==  "Server unavailable":
	print("Server unavailable")
	exit()
	
while True:
	print("What do you want to do?\n1. Send Mail\n2. See Box\n3. See trash\n4. Exit\n")
	cmd = input()
	if cmd == '1':
		os.system("clear")
		mail.sendMail(input("Please put your destination:\n"), input("Please put the subject:\n"), input("Please put the message:\n"))
	elif cmd == '2':
		os.system("clear")
		mail.attMailBox()
		mail.displaySubs()
		if not mail.subjects:
			print("You dont have mails")
		else:
			index = input("What mail do you want to read?\n")
			print(mail.getBody(index))
			cmd = input("Do you want to delete the mail?\nY or N\n")
			if cmd == "Y":
				mail.delFromId(index)
		memes = input("Press enter to return to menu\n")
		os.system("clear")
	elif cmd == '3':
		os.system("clear")
		mail.attMailTrash()
		mail.displaySubs()
		if not mail.subjects:
			print("You dont have mails")
		else:
			index = input("What mail do you want to read?\n")
			print(mail.getBody(index))
		memes = input("Press enter to return to menu\n")
		os.system("clear")
	elif cmd == '4':
		mail.disconnect()
		exit()
