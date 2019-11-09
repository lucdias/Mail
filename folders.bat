@ECHO OFF
IF %1 == client (
	IF NOT EXIST Rmail (
	    mkdir Rmail
	    mkdir Rmail\CaixaPostal Rmail\Lixo
	    ECHO Criando pasta do diretorio
	)
) ELSE (
	IF NOT EXIST SRmail (
	    mkdir SRmail
	)
)
