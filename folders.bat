@ECHO OFF
ECHO Welcome to the mail
IF EXIST Rmail (
    ECHO Pasta de email existe
) ELSE (
    mkdir Rmail
    mkdir Rmail\CaixaPostal Rmail\Lixo
    ECHO Criando pasta do diretorio
)