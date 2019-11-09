HEADERSIZE = 35
import platform

if platform.system() == 'Linux':
	system  = 'Linux'
	folders = "bash folders.sh"
	users   = "bash users.sh"
	bars    = "/"
elif platform.system() == 'Windows':
	system  = 'Windows'
	folders = "folders.bat"
	users   = "users.bat"
	bars    = "\\"

path = "Rmail/CaixaPostal"
noMail = "zero emails"
endMails = "END"
