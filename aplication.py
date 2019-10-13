import client
import mail
import platform
import os
import constant

if platform.system() == 'Linux':
	os.system("bash folders.sh client")
elif platform.system() == 'Windows':
	os.system("folders.bat")

def intro(socket, email):
	print("Welcome to the Mail\nWho are you?")
	email.setUser(input())
	socket.sendMessage(f"GET {email.getUser()}")
	msg = socket.recvMsg()
	while msg != constant.endMails:
		mail.Mail.putIntoMailBox(msg)
		msg = socket.recvMsg()


def menu(client, email):
	print(f"You have {mail.Mail.countMails()} Mail(s)")
	print("\nTo go to mail Box press 1\nTo send a email press 2\n")
	command = input()
	if command == '1':
		mail.Mail.readMailBox()
	elif command == '2':
		print("Put the destination and then the message")
		client.sendMessage(f"SEND {email.getUser()} " + input())


email = mail.Mail()
clientSocket = client.Client()
intro(clientSocket, email)
#os.system("clear")
while True:
	menu(clientSocket, email)
