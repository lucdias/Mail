folder=$(pwd)/SRmail/$1
folderCe=$(pwd)/SRmail/$1/CE
folderLe=$(pwd)/SRmail/$1/LE
if [ -d "$folder" ]
then
	echo Pasta \do usuario existe
else
	mkdir $folder
	mkdir $folderCe
	mkdir $folderLe
	echo Criando pasta \do diretorio
fi
