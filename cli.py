import socket
import sys

# 65 MB
HEADER = 1024*65 #51200 # 50 MB
PORT = 8080

SERVER = socket.gethostbyname(socket.getfqdn()) #"127.0.1.1"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def listagem(acao):
    acao.encode(FORMAT)
    client.send(bytes( acao, FORMAT))

    msg = client.recv(HEADER).decode(FORMAT)
    print(msg)

def envio(acao):
    acao.encode(FORMAT)
    client.send(bytes(acao, FORMAT))

    #Digitar o nome 
    print("Digite o nome:")
    nome = input()

    nome.encode()
    client.send(bytes( nome, FORMAT))


    #if acao == DISCONNECT_MESSAGE:
    print(client.recv(HEADER).decode(FORMAT))
    print()


def saida(msg):
    msg.encode("utf-8")
    client.send(bytes(msg, "utf-8"))
    print(client.recv(HEADER).decode(FORMAT))

# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))

#     client.send(send_length)
#     client.send(message)
#     if msg == DISCONNECT_MESSAGE:
#         print(client.recv(2048).decode(FORMAT))


def sendFile(acao):
    acao.encode(FORMAT)
    client.send(bytes( acao, FORMAT))
    
    print("Nome do arquivo")
    nome = input()
    nome.encode(FORMAT)
    client.send(bytes(nome, FORMAT))

    file = open("entrada.txt", "r")
    newFile = file.read()
    newFile.encode(FORMAT)

    client.send(bytes(newFile, FORMAT))

    msgServer = client.recv(HEADER).decode(FORMAT)
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
        #print("Digite o nome do arquivo:")
        sendFile(acao)
        #send(acao, nome)

    elif msg == 2:
        #print("Digite o nome do diretorio:")
        #nome = input()
        #arq = os.getsize(nome)
        envio(acao)

    elif msg == 3:
        #print("Digite o nome do diretorio o qual quer listar")
        #acao = input()
        listagem(acao)

    elif msg == 4:
        #print("Digite o nome do diretorio:")
        #acao = input()
        envio(acao)
    
    elif msg == 5:
        #print("Digite o nome do diretorio:")
        #acao = input()
        envio(acao)

    elif msg == 0:
        saida(DISCONNECT_MESSAGE)
        
    

