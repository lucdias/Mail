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
	trashBodys = {}
	delMails = {}
	conn = None
	def __init__(self, sock = None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.bind((socket.gethostname(), self.serverPort))
			self.sock.listen(1)
			self.sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock2.bind((socket.gethostname(), 7778))
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
		self.conn.send(bytes(msg, encoding='utf8'))
	
	
	def sendSubjects(self, subjects):
		self.conn.send(pickle.dumps(subjects))
	
	
	def recvMsg(self):
		(messageRecv) = self.conn.recv(2048)
		return (messageRecv.decode())
		
	
	def waitIHB(self):
		(self.conn, addr) = self.sock.accept()
		return 2
		
	
	
	def waitLogin(self):
		(msg) = self.recvMsg()
		self.setLogin(msg)
		self.setLoginFolder()
		return 4
		
		
	def setLoginFolder(self):
		os.system(f"{constant.users} {self.getLogin()}")
	
	
	def sendDns(self):
		self.dnsAddress = "192.168.0.13"
		msg = "REG " + "rafamail.com.br"
		self.sock2.sendto(bytes(msg, encoding='utf8'), (self.dnsAddress,self.dnsPort))
		return 1

	
	def waitMsgs(self):
		(msg) = self.recvMsg()
		msg = msg.split("///", 4)
		if msg[0] == "IOB":
			return 5
		elif msg[0] == "box":
			self.msgIsBox()
		elif msg[0] == "trash":
			self.msgIsTrash()
		elif msg[0] == "SEND":
			self.msgIsSend(msg[1:])
		elif msg[0] == "GET":
			self.msgIsGet(msg[1])
		elif msg[0] == "DEL":
			self.delMsg(msg[1])
			#chamar função que move uma mensagem da caixa de entrada para a lixeira
		return 4

	def delMsg(self, delId):
		handleMsg.handleDel(self.delMails[int(delId)], self.getLogin())
		#excluir o email da pasta 


	def msgIsTrash(self):
		(trashSubjects, trashBodys) = handleMsg.handleTrash(self.getLogin())
		self.setBody(trashBodys)
		self.sendSubjects(trashSubjects)

			
	def msgIsSend(self, msg):
		handleMsg.handleSend(msg[0], msg[1], msg[2], msg[3])
			
	
	def msgIsGet(self, index):
		self.sendMsg(self.getBodyById(index))
	
	
	def msgIsBox(self):
		(subjects, bodys, delBodys) = handleMsg.handleBox(self.getLogin())
		self.setBody(bodys)
		self.setDelBody(delBodys)
		self.sendSubjects(subjects)
			
			
	def reset(self):
		self.setClientAddress()
		self.setLogin()
		self.setBody()
		self.setDelBody()
		return 1
		
	
	def setBody(self, msg = {}):
		self.bodys = msg
	
	
	def setDelBody(self, msg = {}):
		self.delMails = msg
	
	
	def getDelBody(self):
		return self.delMails
	
	
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
		
