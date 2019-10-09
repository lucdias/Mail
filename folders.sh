echo Welcome to the mail
if [ $1 == client ]
then
	folder=$(pwd)/Rmail
	if [ -d "$folder" ]
	then
		echo Pasta de email existe
	else
		mkdir Rmail
		mkdir Rmail/CaixaPostal Rmail/Lixo
		echo Criando pasta \do diretorio
	fi
else
	folder=$(pwd)/SRmail
	if [ -d "$folder" ]
	then
		echo Pasta de email existe
	else
		mkdir SRmail
		echo Criando pasta \do diretorio
	fi
fi
