@ECHO OFF
IF EXIST SRmail\%1 (
	ECHO Pasta do usuario existe
) ELSE (
    mkdir SRmail\%1
    ECHO Criando pasta do diretorio
)
