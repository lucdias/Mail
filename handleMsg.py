import os
import constant
import handleFolder

def checkMsg(msg):
	tempMsg = msg[0:constant.HEADERSIZE]
	command = tempMsg.split()
	if command[0] == "SEND":
		handleSend(command[2], command[1], msg[15:len(msg)])
		return []
	elif command[0] == "GET":
		try:
			return handleGet(command[1])
		except FileNotFoundError:
			os.system(f"mkdir SRmail/{command[1]}")
			handleGet(user)


def handleSend(userTo, userFrom, msg):
	os.system(f"bash users.sh {userTo}")
	fMsg = open(f"SRmail/{userTo}/{userFrom}.txt", "w")
	fMsg.write(f"{userFrom}\n" + f"{msg}")
	fMsg.close()


def handleGet(user):
	path = f"SRmail/{user}/"
	if(handleFolder.countFiles(path) <= 0):
		return [constant.noMail]
	else:
		return handleFolder.readAllFiles(path)
