import socket
import os
import constant
import handleMsg
import handleFolder
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
	
		
	def recvMsg(self):
		try:
			(messageRecv, clientAddress) = self.sock.recvfrom(2048)
			print(messageRecv.decode())
		except socket.timeout:
			print('Server Timeout - line 52')
			return ("Error", "0.0.0.0")
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
			self.setLogin(msg)
			self.sendMsg("OK")
			return 3
		else:
			return 2
		
		
	def setLoginFolder(self):
		os.system(f"{constant.users} {self.getLogin()}")
	
	
	def sendDns(self):
		self.dnsAddress = "172.22.39.144"
		msg = "REG " + "rafamail.com.br"
		print(msg)
		self.sock.sendto(bytes(msg, encoding='utf8'), (self.dnsAddress,self.dnsPort))
		rmsg = self.recvMsg()
		cmd = rmsg[0].split()
		while cmd[0] != "OK":
			self.sock.sendto(bytes(msg, encoding='utf8'), (self.dnsAddress,self.dnsPort))
			rmsg = self.recvMsg()
			cmd = rmsg.split()
		return 1


server = Server()

msf = {
	0 : server.sendDns,
	1 : server.waitIHB,
	2 : server.waitLogin
}	

state = 0	
while True:
	state = msf[state]()
	if state == 3:
		exit()
	
