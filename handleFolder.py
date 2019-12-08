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
	names = []
	with os.scandir(path) as it:
		for entry in it:
			if entry.is_file():
				fMsg = open(path + entry.name, "r")
				msg.append(fMsg.read())
				names.append(entry.name)
				fMsg.close()
		return (msg, names)
