import socket

class Client:
	message = []
	serverName = socket.gethostname()
	serverPort = 7777
	def __init__(self, sock = None):
	    if sock is None:
	        self.sock = socket.socket(
	                        socket.AF_INET, socket.SOCK_DGRAM)
	    else:
	        self.sock = sock
    
    
	def getServerPort(self):
		return self.serverPort


	def connectClient(self, host, port):
		raise NotImplementedError

	
	def createPackets(self, msg):
		if len(msg) > 2048:
			return [msg[i:i+2048] for i in range(0, len(msg), 2048)]
		else:
			return [msg]


	def sendMessage(self, msg):
		self.message = self.createPackets(msg)
		for sendMsg in self.message:
			self.sock.sendto(bytes(sendMsg, encoding='utf8'), (self.serverName, self.serverPort))
		
    
		
    

clientSocket = Client()
print("Send message to the server: ")
while True:
	clientSocket.sendMessage(input())
