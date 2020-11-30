import socket
import sys

# 65 MB
HEADER = 1024*65 
PORTA = 8080

# Inicia um server localhost com o parametro vazio
SERVER = socket.gethostbyname(socket.getfqdn())

ADDR = (SERVER, PORTA)
CODIFICACAO = 'utf-8'
MSG_SAIDA = "DESCONECTAR!"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def listagem(acao):
    acao.encode(CODIFICACAO)
    client.send(bytes( acao, CODIFICACAO))

    msg = client.recv(HEADER).decode(CODIFICACAO)
    print(msg)

def envio(acao):
    # Envia acao
    acao.encode(CODIFICACAO)
    client.send(bytes(acao, CODIFICACAO))

    #Digitar o nome 
    print("Digite o nome:")
    nome = input()
    nome.encode()
    client.send(bytes( nome, CODIFICACAO))

    print(client.recv(HEADER).decode(CODIFICACAO))
    print()


def saida(msg):
    msg.encode("utf-8")
    client.send(bytes(msg, "utf-8"))
    print(client.recv(HEADER).decode(CODIFICACAO))


def sendFile(acao):
    acao.encode(CODIFICACAO)
    client.send(bytes( acao, CODIFICACAO))
    
    print("Nome do arquivo")
    nome = input()
    nome.encode(CODIFICACAO)
    client.send(bytes(nome, CODIFICACAO))

    file = open("entrada.txt", "r")
    newFile = file.read()
    newFile.encode(CODIFICACAO)
    client.send(bytes(newFile, CODIFICACAO))

    msgServer = client.recv(HEADER).decode(CODIFICACAO)
    print(msgServer)

   


print("*** Digite 1 para enviar  aquivo    ***")
print("*** Digite 2 para criar   diretorio ***")
print("*** Digite 3 para listar  diretorio ***")
print("*** Digite 4 para remover arquivo   ***")
print("*** Digite 5 para remover diretorio ***")
print("*** Digite 0 para sair              ***")

msg = int(-1)

while msg != 0:
    print("Digite um numero")

    acao = input()
    msg = int(acao)
    
    if msg == 1:
        sendFile(acao)

    elif msg == 2:
        envio(acao)

    elif msg == 3:
        listagem(acao)

    elif msg == 4:
        envio(acao)
    
    elif msg == 5:
        envio(acao)

    elif msg == 0:
        saida(MSG_SAIDA)
        
    

