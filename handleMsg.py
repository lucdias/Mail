import os
import platform
import constant
import handleFolder
import random

def checkMsg(msg):
	tempMsg = msg[0:constant.HEADERSIZE]
	command = tempMsg.split()
	user = command[1]

	if command[0] == "SEND":
		handleSend(command[2], command[1], msg[constant.HEADERSIZE:len(msg)])
		return []
	elif command[0] == "GET":
		try:
			return handleGet(user)
		except FileNotFoundError:
			os.system("mkdir SRmail" + constant.bars + command[1])
			return handleGet(user)

def handleSend(userTo, userFrom, subject, msg):
	os.system(constant.users + " " + userTo)
	fMsg = open(f"SRmail/{userTo}/CE/{int(random.random()*10000)}.txt", "w")
	fMsg.write(f"{userFrom}\n" + f"{subject}\n" + f"{msg}")
	fMsg.close()


def handleGet(user):
	path = f"SRmail" + constant.bars + user + constant.bars
	if(handleFolder.countFiles(path) <= 0):
		return [constant.noMail]
	else:
		return handleFolder.readAllFiles(path)
		

def handleBox(user):
	msg = handleFolder.readAllFiles(f"SRmail/{user}/CE/")
	bodys = {}
	subjects = []
	index = 0
	for tempMsg in msg:
		otherMsg = tempMsg.split("\n", 3)
		subjects.append((otherMsg[0], otherMsg[1]))
		bodys[index] = otherMsg[2]
		index = index + 1
	return (subjects, bodys)


def handleTrash(user):
	msg = handleFolder.readAllFiles(f"SRmail/{user}/LE/")
	bodys = {}
	subjects = []
	index = 0
	for tempMsg in msg:
		otherMsg = tempMsg.split("\n", 3)
		subjects.append((otherMsg[0], otherMsg[1]))
		bodys[index] = otherMsg[2]
		index = index + 1
	return (subjects, bodys)
	
	
