import socket 
import threading
import sys
import os

#50 MB
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

def criaDir():
    print("Chamou criaDir")
    os.mkdir("teste1")
    # entrar no diretorio
    os.chdir("teste1")
    os.mkdir("KRLLll")
    pass

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
        server.send(bytes(msg, FORMAT))
    # Cria novo arquivo
    #newFile = open(name, "x")

    
    #print(f"Aqui o nome do arquivo {nome}")
    pass

def listaDir():
    print("Chamou listaDir")
    pass

def removeArq():
    print("Chamou removeArq")
    pass

def removeDir():
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
                break


            print(f"tamMsg ************ {tamMsg}")
            
            #msg_length = int(msg_length)
            #msg = conn.recv(msg_length).decode(FORMAT)

            # if msg_length == DISCONNECT_MESSAGE:
            #     #connected = False
            #     conn.send("Desconectando...".encode(FORMAT))
            #     break

            if tamMsg == 1:
                print("ENtrou /******************/")
                
                nameFile = conn.recv(HEADER).decode(FORMAT)
                file = conn.recv(HEADER).decode(FORMAT)
                print("PASSOU DA LEITURA/*/*//*/*/*/*/*/*//*/*")

                enviaArq(nameFile, file, conn)

            elif tamMsg == 2:
                criaDir()

            elif tamMsg == 3:
                listaDir()

            elif tamMsg == 4:
                removeArq()
            
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