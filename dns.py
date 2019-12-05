import socket
import os
import constant
import handleMsg

class dns:
    database = {}
    dnsServerPort = 12000
    destAddress = None
    def __init__(self, sock = None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind((socket.gethostname(), self.dnsServerPort))
        else:
            self.sock = sock
   
    def sendMsg(self, msg):
        self.sock.sendto(bytes(str(msg), encoding='utf8'), self.getDestAddress())
     
    
    def setDestAddress(self, addr):
        self.destAddress = addr
    
    
    def getDestAddress(self):
        return self.destAddress
    
    
    def recvMsg(self):
        (messageRecv, destAddress) = self.sock.recvfrom(2048)
        self.setDestAddress(destAddress)
        return messageRecv.decode("utf-8")

    def register(self, name):
        self.database[name] = self.getDestAddress()
        self.sendMsg("OK")
    


def getFunction(msg):
    tempMsg = msg.split()
    return tempMsg[0]
    
def getArgument(msg):
    tempMsg = msg.split()
    return tempMsg[1]
    
    
    
dnsServer = dns()
print("Run dns Server")
while True:
    msg = dnsServer.recvMsg()
    print(msg)
    if getFunction(msg) == "REG":
        dnsServer.register(getArgument(msg))
        print("database = ")
        print(dnsServer.database)
    elif getFunction(msg) == "WHO":
        print(getArgument(msg))
        if getArgument(msg) in dnsServer.database:
            dnsServer.sendMsg(dnsServer.database[getArgument(msg)][0])
            print(dnsServer.database[getArgument(msg)][0])
        else:
            dnsServer.sendMsg("NOT FOUND")
            dnsServer.setDestAddress(None)
