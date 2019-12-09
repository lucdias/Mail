import constant
import os
import clientTCP
import time
import pickle
import tkinter as tk
import time

class Mail(tk.Tk):
	user = None
	socket = clientTCP.Client()
	qntMails = None
	mailsBody = {}
	subjects = []
	
	@staticmethod
	def putIntoMailBox(msg):	
		if msg != constant.noMail:
			tempMsg = msg.split()
			fMsg = open(f"{constant.path}/{tempMsg[0]}.txt", "w")
			fMsg.write(msg)
			fMsg.close()

	def setUser(self, user):
		self.user = user
	

	def getUser(self):
		return self.user


	@staticmethod
	def countMails():
		count = 0
		with os.scandir(constant.path) as it:
			for i in it:
				count += 1
		return count


	@staticmethod
	def readMailBox():
		with os.scandir(constant.path) as it:
			for entry in it:
				if entry.is_file():
					fMsg = open(constant.path + "/" + entry.name, "r")
					print(fMsg.read())
					print("\n")
					fMsg.close()

	#modularizar melhor essa parte
	def connect(self):
		self.socket.connectClient("rafamail.com.br")
		self.sendLogin(self)
	
			
	def sendLogin(self):
		self.socket.sendMessage(self.getUser(self))
		
		
	def sendMail(self, destination, subject, body):
		self.socket.sendMessage(f"SEND///{destination}///" + f"{self.user}///" + f"{subject}///" + f"{body}")
		
			
	def disconnect(self):
		print("estou desconectando")
		self.socket.disconnectClient()
	
	
	def eraseMail(self):
		raise NotImplementedError


	def setQntMails(self, numMail):
		self.qntMails = numMail


	def getQuantMails(self):
		return self.qntMails


	def attMailBox(self):
		self.socket.sendMessage("box")
		msg = self.socket.recvSub()
		self.subjects = pickle.loads(msg)
		print(self.subjects)
	
	
	def attMailTrash(self):
		self.socket.sendMessage("trash")
		msg = self.socket.recvSub()
		self.subjects = pickle.loads(msg)
	
	
	def displaySubs(self):
		index = 0
		for msg in self.subjects:
			print(f"{index}: {msg[0]} {msg[1]}")
			index += 1	
	
	
	def getBody(self, index):
		self.socket.sendMessage(f"GET///{index}")
		msg = self.socket.recvMsg()
		return msg
		
	
	def delFromId(self, index):
		self.socket.sendMessage(f"DEL///{index}")
		


class login(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		print("comecei o login")
		label = tk.Label(self, text="Entrar no Email")
		label.pack(pady=100,padx=100)

		txtfld=tk.Entry(self, text="Login", bd=5)
		txtfld.pack()

		button = tk.Button(self, text="Entar",command=lambda: controller.logar(txtfld.get()))
		button.pack()

class lista(tk.Frame):
	def __init__(self, parent, controller, lixeira):
		tk.Frame.__init__(self,parent)
		self.user = tk.Label(self, text="Usuario: " + Mail.getUser(Mail))
		self.user.place(relx=0.0, rely=0.05, anchor='sw')
		if lixeira == False:
			self.buttonLixeira = tk.Button(self, text="Lixeira",command=lambda: controller.listarLixeira())
			self.buttonLixeira.place(relx=0.25, rely=0.055, anchor='sw')
			self.buttonEscrever = tk.Button(self, text="Escrever",command=lambda: controller.escreverEmail())
			self.buttonEscrever.place(relx=0.45, rely=0.055, anchor='sw')
			self.buttonDeslogar = tk.Button(self, text="Deslogar",command=lambda: controller.deslogar())
			self.buttonDeslogar.place(relx=0.65, rely=0.055, anchor='sw')
		else:
			self.buttonVoltar = tk.Button(self, text="Voltar",command=lambda: controller.voltarLista(False))
			self.buttonVoltar.place(relx=0.25, rely=0.055, anchor='sw')
			self.buttonDeslogar = tk.Button(self, text="Deslogar",command=lambda: controller.deslogar())
			self.buttonDeslogar.place(relx=0.45, rely=0.055, anchor='sw')
		y = 0.2
		index = 0
		if not Mail.subjects:
			self.deEassunto = tk.Label(self, text="Caixa de Entrada Vazia")
			self.deEassunto.place(relx = 0.0, rely = y, anchor='sw')
		else:
			for msg in Mail.subjects:
				self.deEassunto = tk.Label(self, text="De: "+msg[0]+"          Assunto: "+msg[1])
				self.deEassunto.place(relx = 0.0, rely = y, anchor='sw')
				self.buttonLer = tk.Button(self, text="Ler",command=lambda x=index: controller.lerEmail(x, lixeira, Mail.subjects[x]))
				self.buttonLer.place(relx = 0.7, rely = y, anchor='sw')
				if lixeira == False:
					self.buttonDelete = tk.Button(self, text="Delete",command=lambda x=index: controller.deletar(x))
					self.buttonDelete.place(relx = 0.8, rely = y, anchor='sw')
				y = y + 0.1
				index = index + 1

class lendoEmail(tk.Frame):
	def __init__(self, parent, controller, index, lixeira, subject):
		tk.Frame.__init__(self,parent)
		self.user = tk.Label(self, text="Usuario: " + Mail.getUser(Mail))
		self.user.place(relx=0.0, rely=0.05, anchor='sw')
		self.buttonVoltar = tk.Button(self, text="Voltar",command=lambda: controller.voltarLista(lixeira))
		self.buttonVoltar.place(relx=0.25, rely=0.055, anchor='sw')
		
		if lixeira == False:
			self.buttonDelete = tk.Button(self, text="Delete",command=lambda: controller.deletar(index))
			self.buttonDelete.place(relx=0.45, rely=0.055, anchor='sw')


		self.remetente = tk.Label(self, text="De: "+subject[0])
		self.remetente.place(relx=0.0, rely=0.2, anchor='sw')

		self.assunto = tk.Label(self, text="Assunto: "+subject[1])
		self.assunto.place(relx=0.0, rely=0.25, anchor='sw')

		self.corpo = tk.Label(self, text=Mail.getBody(Mail, index))
		self.corpo.place(relx=0.0, rely=0.35, anchor='sw')

class escrevendo(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self,parent)
		self.button = tk.Button(self, text="Voltar",command=lambda: controller.voltarLista(False))
		self.button.place(relx=0.5, rely=0.05, anchor='sw')

		self.label1 = tk.Label(self, text="De: "+Mail.getUser(Mail))
		self.label1.place(relx=0.0, rely=0.08, anchor='sw')

		self.label2 = tk.Label(self, text="Para: ")
		self.label2.place(relx=0.0, rely=0.16, anchor='sw')
		self.remetente=tk.Entry(self, text="", bd=5)
		self.remetente.place(relx=0.15, rely=0.16, anchor='sw')

		self.label3 = tk.Label(self, text="Assunto: ")
		self.label3.place(relx=0.0, rely=0.24, anchor='sw')
		self.assunto=tk.Entry(self, text="", bd=5)
		self.assunto.place(relx=0.15, rely=0.24, anchor='sw')

		self.label4 = tk.Label(self, text="Corpo da mensagem: ")
		self.label4.place(relx=0.0, rely=0.32, anchor='sw')

		self.corpo = tk.Text(self, height=18, width=62)
		self.corpo.place(relx=0.0, rely=1.0, anchor='sw')
		
		self.enviar = tk.Button(self, text="Enviar",command=lambda: controller.enviarEVoltar(self.remetente.get(), self.assunto.get(), self.corpo.get("1.0",'end-1c')))
		self.enviar.place(relx=0.5, rely=0.32, anchor='sw')


class Interface(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.container = tk.Frame(self)

		self.container.pack(side="top", fill="both", expand = True)

		self.container.grid_rowconfigure(0, weight=1)
		self.container.grid_columnconfigure(0, weight=1)


		#Tela de Login
		self.frameLogin = login(self.container, self)
		self.frameLogin.grid(row=0, column=0, sticky="nsew")
		self.frameLogin.tkraise()

	def logar(self, loginName):
		Mail.setUser(Mail, loginName)
		print(Mail.connect(Mail))
		time.sleep(1)
		Mail.attMailBox(Mail)

		self.frameLista = lista(self.container, self, False)
		self.frameLista.grid(row=0, column=0, sticky="nsew")
		self.frameLista.tkraise()

	def deslogar(self):
		Mail.disconnect(Mail)
		exit()
		'''self.frameLogin = login(self.container, self)
		self.frameLogin.grid(row=0, column=0, sticky="nsew")
		self.frameLogin.tkraise()'''

	def lerEmail(self, index, lixeira, subject):
		self.frameLendoEmail = lendoEmail(self.container, self, index, lixeira, subject)
		self.frameLendoEmail.grid(row=0, column=0, sticky="nsew")
		self.frameLendoEmail.tkraise()

	def deletar(self, index):
		Mail.delFromId(Mail, index)
		Mail.attMailBox(Mail)
		self.frameLista = lista(self.container, self, False)
		self.frameLista.grid(row=0, column=0, sticky="nsew")
		self.frameLista.tkraise()

	def voltarLista(self, lixeira):
		if lixeira == True:
			Mail.attMailTrash(Mail)
			self.frameLista = lista(self.container, self, True)
			self.frameLista.grid(row=0, column=0, sticky="nsew")
			self.frameLista.tkraise()
		else:
			Mail.attMailBox(Mail)
			self.frameLista = lista(self.container, self, False)
			self.frameLista.grid(row=0, column=0, sticky="nsew")
			self.frameLista.tkraise()

	def listarLixeira(self):
		Mail.attMailTrash(Mail)
		self.frameLista = lista(self.container, self, True)
		self.frameLista.grid(row=0, column=0, sticky="nsew")
		self.frameLista.tkraise()

	def escreverEmail(self):
		self.frameLista = escrevendo(self.container, self)
		self.frameLista.grid(row=0, column=0, sticky="nsew")
		self.frameLista.tkraise()

	def enviarEVoltar(self, remetente, assunto, corpo):
		Mail.sendMail(Mail, remetente, assunto, corpo)
		Mail.attMailBox(Mail)
		self.frameLista = lista(self.container, self, False)
		self.frameLista.grid(row=0, column=0, sticky="nsew")
		self.frameLista.tkraise()


interface = Interface()

interface.geometry("500x500")
interface.mainloop()

'''mail = Mail()
mail.setUser(input("Please put your user:\n"))
mail.connect()
while True:
	print("What do you want to do?\n1. Send Mail\n2. See Box\n3. See trash\n4. Exit\n")
	cmd = input()
	if cmd == '1':
		mail.sendMail(input("Please put your destination:\n"), input("Please put the subject:\n"), input("Please put the message:\n"))
	elif cmd == '2':
		mail.attMailBox()
		mail.displaySubs()
		index = input("What mail do you want to read?\n")
		print(mail.getBody(index))
		cmd = input("Do you want to delete the mail?\nY or N\n")
		if cmd == "Y":
			mail.delFromId(index)
	elif cmd == '3':
		mail.attMailTrash()
		mail.displaySubs()
		index = input("What mail do you want to read?\n")
		print(mail.getBody(index))
	elif cmd == '4':
		mail.disconnect()
		exit()'''
