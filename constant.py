import platform

if platform.system() == 'Linux':
	system = 'Linux'
elif platform.system() == 'Windows':
	system = 'Windows'

HEADERSIZE = 15
path = "Rmail/CaixaPostal"
noMail = "zero emails"
endMails = "END"
