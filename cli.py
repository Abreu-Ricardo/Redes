import socket
import sys
import os
import time

# 65 MB
HEADER = 1024*4#*65 
PORTA = int(sys.argv[1])  # colocar para receber como int(sys.arg[2])

# Inicia um server localhost com o parametro vazio
SERVER = socket.gethostbyname(socket.getfqdn())
#SERVER = '127.0.1.1'  # colocar para recever int(sys.arg[1])

ADDR = (SERVER, PORTA)
CODIFICACAO = 'utf-8'
MSG_SAIDA = "SAIR"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def listagem(acao):
    acao.encode(CODIFICACAO)
    client.send(bytes( acao, CODIFICACAO))

    #try:
    msg = client.recv(HEADER).decode(CODIFICACAO)
    print(msg)
    #except Exception as e:
     #   print(e)

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
    #msg.encode("utf-8")
    client.send(bytes(msg, "utf-8"))
    print(client.recv(HEADER).decode(CODIFICACAO))


def sendFile(acao):
    # envia acao
    acao.encode(CODIFICACAO)
    client.send(bytes( acao, CODIFICACAO))
    
    # envio do nome
    print("Nome do arquivo")
    nome = input()
    nome.encode(CODIFICACAO)
    client.send(bytes(nome, CODIFICACAO))

    # *** ABRINDO ARQUIVO PARA ENVIO ***

    # t = open(nome, "rb")
    # f = t.read(HEADER)
    # client.send(f)


    # with open(nome,"rb") as f:
    #     #dado = f.read()
    #     client.sendfile(f)
    #     pass

    try:
        print("Enviando aguarde...")

        f = open(nome, "rb")
        data = f.read()
        client.sendall(data)

        time.sleep(5)

        a = b'0'
        client.send(a)
        #client.send(bytes(a, CODIFICACAO))

        #print(client.recv(HEADER).decode())

    except Exception as e:

        print("Nao foi possivel enviar arquivo!")
        return

    # dado = b'0' * HEADER
    # saida("0")
    # print(dado)
    # client.send(dado)
    # tam = os.stat(nome)
    # print(tam.st_size )
    # print((tam.st_size / 1024) )

    # tu = int((tam.st_size / 1024) )
    # t  = str((tam.st_size / 1024) )

    # client.send(bytes(t, CODIFICACAO))

    # with open(nome, "rb") as f:
    #     dado = f.read(HEADER)
    #     client.send(dado)
        

    #     while dado:
    #         client.sendall(dado)
    #         dado = f.read(HEADER)
    #     #client.send(bytes(None, CODIFICACAO))
    #     #client.send(b'')
    #     print("Passou!")
   
   
   
    # f = open(nome, "rb")
    # for x in range(0,tu):
    #     dado = f.read(HEADER)
    #     client.send(dado)

    # print("Enviou tudo!")


    


    #print(client.recv(HEADER).decode())

    
    # with open(nome, "rb") as f:
    #     text = f.read(1024)
    #     while text:

    #         client.send(text)

    #         print(f"Enviado {text}")
    #         text = f.read(HEADER)

    #         if not text:
    #             break

    # print("Acabou de enviar!")

    #  with open(filename, "rb") as f:
    #     text = f.read(HEADER)

    #     while text:
    #         conexao.send(text)
    #         print(f"Enviado {text}")
    #         text = f.read(HEADER)
    #         #text.encode()
    #     f.close()
   

    # with open(nome, "rb") as f:
    #     #for x in f:
    #     while True:
    #         #dado = x
    #         #print(x)
    #         dado = f.read(HEADER)

    #         # Se acabar os dados lidos
    #         if not dado:
    #             print(dado)
    #             #client.send("sai".encode())
    #             break

    #         client.send(dado)


   


print("*** Digite 1 para enviar  arquivo   ***")
print("*** Digite 2 para criar   diretorio ***")
print("*** Digite 3 para listar  diretorio ***")
print("*** Digite 4 para remover arquivo   ***")
print("*** Digite 5 para remover diretorio ***")
print("*** Digite 6 para mudar   diretorio ***")
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

    elif msg == 6:
        envio(acao)

    elif msg == 0:
        saida("0")
        
    

