import socket 
import threading
import sys
import os
import select

#65 MB
HEADER = 1024*4#*65
PORTA = int(sys.argv[1]) # colocar para receber como int(sys.arg[2])

# Inicia um server localhost com o parametro vazio
SERVER =  socket.gethostbyname(socket.getfqdn())
#SERVER = '127.0.0.1' # colocar para recever int(sys.arg[1])

ADDR = (SERVER, PORTA)
CODIFICACAO = 'utf-8'
MSG_SAIDA = "SAIR"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Faz o link com ADDR
server.bind(ADDR)


def mudaDir(nomeDir, conexao):
    dirAtual = os.listdir()

    try:
        os.chdir(nomeDir)
        
        caminho = os.getcwd()
        conexao.send(f"Diretorio atual {caminho}".encode())

        # for x in dirAtual:
        #     #print(x)
            
        #     if  x == nomeDir and os.path.isdir(x):
        #         print(f"Achou!!!!!!!!!!! {x}")
        #         os.chdir(x)
        #         caminho = os.getcwd()
        #         print(caminho)
        #         conexao.send(f"Diretorio atual {caminho}".encode())
        #         return

    except Exception as e:
        print(e)
        conexao.send("Nao foi possivel mudar de diretorio!".encode())
        


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
def enviaArq(file,  conexao):
    print(f"Chamou criaArq // NOME PASSADO -> {file}\n")
    print()
    print()
    print()
    print()

    
    try:
        os.mkdir("teste1")
        os.chdir("teste1")

        
        cont = int(0)
        tam = 1024
        mensagem = conexao.recv(HEADER)
        print(mensagem)

        with open(file, "wb") as f:
            f.write(mensagem)
            
            while mensagem:
                mensagem = conexao.recv(HEADER)

                if mensagem == b'0':
                    break
                print(mensagem)

                f.write(mensagem)

        conexao.send(f"Arquivo enviado!".encode())



        # tam = int(float(conexao.recv(15).decode()))
        # print(tam)





        #************************************************
        # f = open(file, "wb")

        # for i in range(0, tam):
        #     print(i)
        #     data = conexao.recv(HEADER)
        #     f.write(data)

        # f.close

        # while True:
        #     cont+=1
        #     print("1")
        #     asd = conexao.recv(HEADER)
        #     print("2")
        #     print(cont)
        #     print(asd)

        #     if asd == b'':
        #         print("entrou no if de saida")
        #         f.close()
        #         return

        #     f.write(asd)

        

        # voltar para o diretorio que o iniciou
        os.chdir("..")
        return

    except Exception as e:
        print(e)
        #conexao.send(f"{e}".encode())
        return



    print("Acabou envia arquivo!")
    
    #return

def listaDir(conexao):

    try:
        msg = os.listdir(".")
        print()

        # Caso o diretorio estiver vazio, nao havera itens no array
        if msg != []:
            with open("lista", "w+") as f:
                for i in msg:
                    f.write(i)
                    f.write("\n")

            with open("lista", "r") as f:
                text = f.read()
                conexao.send(text.encode())
            os.remove("lista")

        else:
            conexao.send(bytes("Diretorio vazio!", CODIFICACAO))
            return

    except Exception as e:
        print(e)
        conexao.send("Nao foi possivel listar diretorio!".encode())

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
        conexao.send(f"{e}".encode())

        # conexao.send("Diretorio nao pode ser removido!".encode(CODIFICACAO))
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

        print("Esperando requisicao...")
        msg_length = conexao.recv(HEADER)#.decode(CODIFICACAO)

        print(f"AQUI MSG_LENGTH---->>>>> {msg_length}")

        # Se nao for a mensagem de desconexao faz alguma acao
        if msg_length:
            msg_length = msg_length.decode(CODIFICACAO)
            
            if msg_length != "0":

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
                #file = conexao.recv(HEADER)

                enviaArq(nameFile,  conexao)

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

            elif tamMsg == 6:
                nomeDir = conexao.recv(HEADER).decode(CODIFICACAO)

                mudaDir(nomeDir, conexao)
        
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
