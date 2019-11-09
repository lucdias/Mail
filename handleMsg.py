import os
import platform
import constant
import handleFolder

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

def handleSend(userTo, userFrom, msg):
	os.system(constant.users + " " + userTo)
	fMsg = open(f"SRmail/{userTo}/{userFrom}.txt", "w")
	fMsg.write(f"{userFrom}\n" + f"{msg}")
	fMsg.close()


def handleGet(user):
	path = f"SRmail" + constant.bars + user + constant.bars
	if(handleFolder.countFiles(path) <= 0):
		return [constant.noMail]
	else:
		return handleFolder.readAllFiles(path)
