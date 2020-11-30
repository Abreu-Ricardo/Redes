import socket 
import threading
import sys
import os

#65 MB
HEADER = 1024*65#51200 #sys.argv[1] # Passar como argumento na linha de comando, tamanho do buffer
PORT = 8080
# SERVER =  socket.gethostbyname(socket.gethostname())

# Inicia um server localhost com o parametro vazio
SERVER =  socket.gethostbyname(socket.getfqdn())

ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def criaDir(nomeDir, conn):
    try:
        os.mkdir(nomeDir)

        msg = "Diretorio criado!"
        msg.encode()
        conn.send(bytes( msg, FORMAT))

    except Exception as e:
        print(e)
        msg = "Nao foi possivel criar diretorio!"
        msg.encode()
        conn.send(bytes( msg, FORMAT))

#Arquivo
def enviaArq(file, buffer, conn):
    print(f"Chamou criaArq// NOME PASSADO -> {file}")
    print()
    print()
    print()
    print()
    print(f"BUFFER AQUI KARAIO ---->>> {buffer}")

    try:
        arquivo = open(file, "x+")
        arquivo.write(buffer)

        alerta = "Aquivo enviado!"
        alerta.encode(FORMAT)
        conn.send(bytes(alerta, "utf-8"))

    except Exception as e:
        print(e)

        msg = "Arquivo ja enviado"
        msg.encode(FORMAT)
        conn.send(bytes(msg, FORMAT))
    # Cria novo arquivo
    #newFile = open(name, "x")

    
    #print(f"Aqui o nome do arquivo {nome}")
    pass

def listaDir(conn):

    lista = open("lista", "w")
    msg = os.listdir(".")
    print()

    for i in msg:
        lista.write(i)
        lista.write("\n")

    lista.close()
        
    f = open("lista", "r")
    texto = f.read()

    texto.encode(FORMAT)

    conn.send(bytes( texto, 'utf-8'))
    os.remove("lista")

    # print("*************************Chamou listaDir")
    return

# Passar nome do arquivo a ser deletado
def removeArq(nameFile, conn):
    try:
        os.remove(nameFile)

        msg = "Arquivo removido!"
        msg.encode(FORMAT)
        conn.send(bytes( msg, FORMAT))
        
    except Exception as e:

        print(e)

        msg = "Nao foi possivel remover arquivo!"
        msg.encode(FORMAT)
        conn.send(bytes( msg, FORMAT))

    
    print("Chamou removeArq")
    return

def removeDir():

    #os.rmdir(nameDir)
    print("Chamou removeDir")
    pass

def handle_client(conn, addr):
    #print(f"[NEW CONNECTION] {addr} connected.")
    print(f"Cliente conectado a {addr}")
    
    connected = True
    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)

        print(f"AQUI MSG_LENGTH_____>>>>> {msg_length}")

        # Se nao for a mensagem de desconexao faz alguma acao
        if msg_length:

            if msg_length != DISCONNECT_MESSAGE:
                tamMsg = int(msg_length)
            else:
                print("Cliente desconectando...")
                conn.send("Desconectando...".encode(FORMAT))
                print()
                break

            print(f"tamMsg ************ {tamMsg}")
            
            # Envia arquivo
            if tamMsg == 1:
                
                nameFile = conn.recv(HEADER).decode(FORMAT)
                file = conn.recv(HEADER).decode(FORMAT)

                enviaArq(nameFile, file, conn)

            # Cria diretorio
            elif tamMsg == 2:
                nomeDir = conn.recv(HEADER).decode(FORMAT)

                criaDir(nomeDir, conn)

            # Lista diretorio
            elif tamMsg == 3:

                # nameDir = conn.recv(HEADER).decode(FORMAT)
                listaDir(conn)
                

            # Remove arquivo
            elif tamMsg == 4:
                nameFile = conn.recv(HEADER).decode(FORMAT)
                removeArq(nameFile, conn)
            
            # Remove diretorio
            elif tamMsg == 5:
                removeDir()
            # Mensagem recebida
            #print(f"Mensagem de [{addr}] {msg_length}")
        
        else:
            conn.send("Desconectando...".encode(FORMAT))
            break

    conn.close()
        

def start():
    server.listen()
    #print(f"[LISTENING] Server is listening on {SERVER}")
    print(f"Conectado a {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() # Inicia a execucao da thread

        #print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        print(f"Clientes conectados {threading.activeCount() - 1}")
        #acao = 


#print("[STARTING] server is starting...")
print("Subindo servidor...")
#HEADER = int(sys.argv[1])
print(f"tam header {HEADER} ")
start()
