import socket
import os
import constant
import handleMsg
import handleFolder
import pickle
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
	bodys = {}
	
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock.bind((socket.gethostname(), self.serverPort))
			self.sock.settimeout(5.0)
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
	
	
	def sendSubjects(self, subjects):
		self.sock.sendto(pickle.dumps(subjects), self.getClientAddress())
	
	
	def recvMsg(self):
		try:
			(messageRecv, clientAddress) = self.sock.recvfrom(2048)
			print(messageRecv.decode())
		except socket.timeout:
			print('Server Timeout - line 52')
			return ("timeout", "0.0.0.0")
		else:
			return (messageRecv.decode(), clientAddress)
		
	
	def waitIHB(self):
		(msg, addr) = self.recvMsg()
		if msg == "IHB":
			self.clientAddress = addr
			self.sendMsg("IHB")
			return 2
		else:
			return 1
	
	
	def waitLogin(self):
		(msg, addr) = self.recvMsg()
		if addr == self.clientAddress:
			if msg == "IHB":
				self.sendMsg("IHB")
				return 2
			else:
				self.setLogin(msg)
				self.setLoginFolder()
				self.sendMsg("ACK")
			return 4
		else:
			return 2
		
		
	def setLoginFolder(self):
		os.system(f"{constant.users} {self.getLogin()}")
	
	
	def sendDns(self):
		self.dnsAddress = "192.168.0.13"
		msg = "REG " + "rafamail.com.br"
		print(self.dnsAddress)
		self.sock.sendto(bytes(msg, encoding='utf8'), (self.dnsAddress,self.dnsPort))
		return 1

	
	def waitMsgs(self):
		(msg, addr) = self.recvMsg()
		if msg == "timeout":
			return msg
		msg = msg.split("///", 4)
		if addr != self.getClientAddress():
			return 4
		elif msg[0] == "IOB":
			return 5
		elif msg[0] == "box":
			self.msgIsBox()
			return 4
		elif msg[0] == "trash":
			return 4
		elif msg[0] == "SEND":
			self.msgIsSend(msg[1:])
			self.sendMsg("ACK")
			return 4
		elif msg[0] == "GET":
			self.msgIsGet(msg[1])
			return 4
		elif msg[0] == self.getLogin():
			self.sendMsg("ACK")
			return 4
		elif msg[0] == "IHB":
			self.sendMsg("ACK")
			return 2
			
	def msgIsSend(self, msg):
		handleMsg.handleSend(msg[0], msg[1], msg[2], msg[3])
			
	
	def msgIsGet(self, index):
		self.sendMsg(self.getBodyById(index))
	
	
	def msgIsBox(self):
		(subjects, bodys) = handleMsg.handleBox(self.getLogin())
		self.setBody(bodys)
		self.sendSubjects(subjects)
			
			
	def reset(self):
		self.sendMsg("IOB")
		(msg, addr) = self.recvMsg()
		count = 0
		while msg == "timeout" and count < 6:
			(msg, addr) = self.recvMsg()
			count += 1
		if msg == "IOB":
			return 5
		self.setClientAddress()
		self.setLogin()
		return 1
		
	
	def setBody(self, msg = {}):
		self.bodys = msg
	
	
	def getBody(self):
		return self.bodys
	
	
	def getBodyById(self, index):
		return self.bodys[int(index)]
		
server = Server()

msf = {
	0 : server.sendDns,
	1 : server.waitIHB,
	2 : server.waitLogin,
	4 : server.waitMsgs,
	5 : server.reset
}	

state = 0
count = 0
while True:
	state = msf[state]()
	if state == "timeout":
		count += 1
		
