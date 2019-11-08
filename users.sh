folder=$(pwd)/SRmail/$1

if [ -d "$folder" ]
then
	echo Pasta \do usuario existe
else
	mkdir $folder
	echo Criando pasta \do diretorio
fi
