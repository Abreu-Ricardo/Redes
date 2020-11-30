import socket 
import threading
import sys
import os

#65 MB
HEADER = 1024*65
PORTA = 8080

# Inicia um server localhost com o parametro vazio
SERVER =  socket.gethostbyname(socket.getfqdn())

ADDR = (SERVER, PORTA)
CODIFICACAO = 'utf-8'
MSG_SAIDA = "DESCONECTAR!"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz o link com ADDR
server.bind(ADDR)


def mudaDir(nomeDir):
    dirAtual = os.listdir()

    for x in dirAtual:
        print(x)
        
        if  x == nomeDir and os.path.isdir(x):
            print(f"Achou!!!!!!!!!!! {x}")
            print(os.getcwd())
            os.chdir(x)


def criaDir(nomeDir, conexao):

    try:
        os.mkdir(nomeDir)
        conexao.send("Diretorio criado!".encode(CODIFICACAO))

    except Exception as e:
        print(e)
        msg = "Nao foi possivel criar diretorio!"
        msg.encode()
        conexao.send("Nao foi possivel criar diretorio!".encode(CODIFICACAO))

#Arquivo
def enviaArq(file, buffer, conexao):
    print(f"Chamou criaArq// NOME PASSADO -> {file}")
    print()
    print()
    print()
    print()
    print(f"BUFFER AQUI KARAIO ---->>> {buffer}")

    try:
        arquivo = open(file, "x+")
        arquivo.write(buffer)
        conexao.send("Aquivo enviado!".encode(CODIFICACAO))

    except Exception as e:
        print(e)
        conexao.send("Arquivo ja enviado".encode(CODIFICACAO))
    
    pass

def listaDir(conexao):

    lista = open("lista", "w")
    msg = os.listdir(".")
    print()

    for i in msg:
        lista.write(i)
        lista.write("\n")

    lista.close()
        
    f = open("lista", "r")
    texto = f.read()

    texto.encode(CODIFICACAO)

    conexao.send(bytes( texto, 'utf-8'))
    os.remove("lista")

    return

# Passar nome do arquivo a ser deletado
def removeArq(nameFile, conexao):
    try:
        os.remove(nameFile)
        conexao.send("Arquivo removido!".encode(CODIFICACAO))

    except Exception as e:

        print(e)

        msg = "Nao foi possivel remover arquivo!"
        msg.encode(CODIFICACAO)
        conexao.send(bytes( msg, CODIFICACAO))

    
    print("Chamou removeArq")
    return

def removeDir(nameDir, conexao):
    
    try:
        os.rmdir(nameDir)
        conexao.send("Diretorio removido!".encode(CODIFICACAO))

    except Exception as e:

        print(e)
        # arquivos = os.listdir()

        # # Caso o diretorio nao seja vazio
        # for x in arquivos:
        #     os.remove(x)
        
        # # Volta para o diretorio pai
        # os.chdir("..")

        # #Deleta o diretorio escolhido
        # os.rmdir(nameDir)

        

    print("Chamou removeDir")
    return

def escuta_cliente(conexao, addr):
    print(f"Cliente conectado a {addr}")
    
    conectado = True
    while conectado:

        msg_length = conexao.recv(HEADER).decode(CODIFICACAO)

        print(f"AQUI MSG_LENGTH---->>>>> {msg_length}")

        # Se nao for a mensagem de desconexao faz alguma acao
        if msg_length:

            if msg_length != MSG_SAIDA:
                tamMsg = int(msg_length)
            else:
                print(f"Cliente {threading.activeCount() -1 } desconectando...")
                conexao.send("Desconectando...".encode(CODIFICACAO))
                print()
                break

            print(f"tamMsg ************ {tamMsg}")
            
            # Envia arquivo
            if tamMsg == 1:
                
                nameFile = conexao.recv(HEADER).decode(CODIFICACAO)
                file = conexao.recv(HEADER).decode(CODIFICACAO)

                enviaArq(nameFile, file, conexao)

            # Cria diretorio
            elif tamMsg == 2:

                nomeDir = conexao.recv(HEADER).decode(CODIFICACAO)
                criaDir(nomeDir, conexao)

            # Lista diretorio
            elif tamMsg == 3:
                listaDir(conexao)
                

            # Remove arquivo
            elif tamMsg == 4:
                nameFile = conexao.recv(HEADER).decode(CODIFICACAO)
                removeArq(nameFile, conexao)
            
            # Remove diretorio
            elif tamMsg == 5:

                nome = conexao.recv(HEADER).decode(CODIFICACAO)
                print(f"ASUDIAUSDUASD {nome}")

                removeDir(nome, conexao)
        
        else:
            conexao.send("Desconectando...".encode(CODIFICACAO))
            break

    conexao.close()
        

def start():
    # Ouve requisicoes de ADDR
    server.listen()
    print(f"Conectado a {SERVER}")
    
    while True:
        conexao, addr = server.accept()
        thread = threading.Thread(target=escuta_cliente, args=(conexao, addr))
        thread.start() # Inicia a execucao da thread

        print(f"Clientes conectados {threading.activeCount() - 1}")


print("Subindo servidor...")
print(f"tam header {HEADER} ")
start()
