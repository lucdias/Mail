import os
import constant

def countFiles(path):
	count = 0
	with os.scandir(path) as it:
		for i in it:
			count = count + 1
	return count


def readAllFiles(path):
	msg = []
	with os.scandir(path) as it:
		for entry in it:
			if entry.is_file():
				fMsg = open(path + entry.name, "r")
				msg.append(fMsg.read())
				fMsg.close()
		msg.append(constant.endMails)
		return msg
