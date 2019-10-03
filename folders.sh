echo Welcome to the mail
folder=$(pwd)/Rmail
if [ -d "$folder" ]
then
    echo Pasta de email existe
else
    mkdir Rmail
    mkdir Rmail/CaixaPostal Rmail/Lixo
    echo Criando pasta \do diretorio
fi