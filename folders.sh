echo Welcome to the mail
if [ $1 == client ]
then
	folder=$(pwd)/Rmail
	if [ -d "$folder" ]
	then
		:
	else
		mkdir Rmail
		mkdir Rmail/CaixaPostal Rmail/Lixo
	fi
else
	folder=$(pwd)/SRmail
	if [ -d "$folder" ]
	then
		:
	else
		mkdir SRmail
	fi
fi
