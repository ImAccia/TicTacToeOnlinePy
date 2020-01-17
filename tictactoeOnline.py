from threading import Thread
import time
import socket
import sys
import os


i = 0
board = [" "," "," "," "," "," "," "," "," "]
turno = False

class myThread (Thread):
    def __init__(self, nome, ip):
        Thread.__init__(self)
        self.nome = nome
        self.ip = ip

    def run(self):
        
        if self.name == "Thread-1":
            global i
            global board
            global turno
            # Creazione socket TCP/IP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Connessione alla porta della socket sulla quale il server è in ascolto
            server_address = (self.ip, 10000)
            print('Connessione a {} : {}'.format(*server_address))
            sock.connect(server_address)

            print("Scrivere il messaggio che si desidera mandare: ")
            printed = False
            while True:
                if turno:
                    try:
                        # Send data
                        message = input().encode()
                        sock.sendall(message)
                        if int(message) < 10 and int(message) > 0:
                            if i % 2 == 0:
                                #controllo che la posizone scelta sia vuota
                                if board[int(message)-1] == " ":
                                    board[int(message)-1] = "x"
                                    i=i+1
                                else:
                                    print("Posizione occupata")
                            else:
                                if board[int(message)-1] == " ":
                                    board[int(message)-1] = "o"
                                    i=i+1
                                else:
                                    print("Posizione occupata")
                        else:
                            print("Posizione invalida")

                        clear = lambda: os.system('cls')
                        clear()

                        print("\t"+board[0]+"\t|\t"+board[1]+"\t|\t"+board[2]+"\n"+"\t"+board[3]+"\t|\t"+board[4]+"\t|\t"+board[5]+"\n"+"\t"+board[6]+"\t|\t"+board[7]+"\t|\t"+board[8]+"\n")
                        #controllo vittoria
                        j = 0
                        vittoria = False

                        #orizzontale
                        while j < 9:
                            if board[j] == board[j+1] and board[j+1] == board[j+2] and board[j] != " " and vittoria != True:
                                print("Vittoria orizzontale")
                                vittoria = True
                                print(str(j))
                            j=j+3

                        #verticale
                        for k in range(3):
                            if board[k] == board[k+3] and board[k+3] == board[k+6] and board[k] != " " and vittoria != True:
                                print("Vittoria verticale")
                                vittoria = True


                        #diagonale
                        if (board[0] == board[4] and board[4] == board[8] or board[2] == board[4] and board[4] == board[6]) and board[4] != " " and vittoria!=True:
                            print("Vittoria diagonale")
                            vittoria = True

                        turno = False
                            
                    finally:
                        flag = True
                        if flag == False:
                            socket.close()

        else:
            i
            board
            turno
            # Creazione socket TCP/IP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Unione della porta alla socket
            server_address = (self.ip, 10000)
            sock.bind(server_address)

            # Ascolta per connessioni in arrivo
            sock.listen(1)

            while True:
                # Aspetta la connessione
                connection, client_address = sock.accept()
                try:
                    stampa = ""
                    while True:
                        try:
                            #ricevo input
                            data = int(connection.recv(1024))
                            clear = lambda: os.system('cls') #on Windows System
                            clear()
                            if type(data) == int:
                                #controllo che sia valido
                                if data > 0 and data < 10:

                                    #controllo se è il turno delle x o delle o
                                    if i % 2 == 0:

                                        #controllo che la posizone scelta sia vuota
                                        if board[data-1] == " ":
                                            board[data-1] = "x"
                                            i=i+1
                                            turno = True
                                    else:
                                        if board[data-1] == " ":
                                            board[data-1] = "o"
                                            i=i+1
                                            turno = True

                                    #stampo il campo
                                    stampa = ""
                                    stampa = stampa +"\t"+board[0]+"\t|\t"+board[1]+"\t|\t"+board[2]+"\n"+"\t"+board[3]+"\t|\t"+board[4]+"\t|\t"+board[5]+"\n"+"\t"+board[6]+"\t|\t"+board[7]+"\t|\t"+board[8]+"\n"  
                                    #send = stampa+";"+str(i)
                                    print(stampa)
                                    #connection.sendall(send.encode())
                                    
                                    #controllo vittoria
                                    j = 0
                                    vittoria = False

                                    #orizzontale
                                    while j < 9:

                                        if board[j] == board[j+1] and board[j+1] == board[j+2] and board[j] != " " and vittoria != True:
                                            print("Vittoria orizzontale")
                                            connection.sendall("Vittoria orizzontale".encode())
                                            vittoria = True
                                            print(str(j))
                                        j=j+3

                                    #verticale
                                    for k in range(3):
                                        if board[k] == board[k+3] and board[k+3] == board[k+6] and board[k] != " " and vittoria != True:
                                            print("Vittoria verticale")
                                            connection.sendall("Vittoria verticale".encode())
                                            vittoria = True


                                    #diagonale
                                    if (board[0] == board[4] and board[4] == board[8] or board[2] == board[4] and board[4] == board[6]) and board[4] != " " and vittoria!=True:
                                        print("Vittoria diagonale")
                                        connection.sendall("Vittoria diagonale".encode())
                                        vittoria = True
                                else:
                                    #input errato
                                    connection.sendall("Inserire un valore compreso tra 1 e 9".encode())
                            else:
                                #input errato
                                connection.sendall("Inserire un valore numerico".encode())
                        except:
                            #input errato
                            connection.sendall("Inserire un valore numerico".encode())
                except:
                    print()


ipG = input("Inserire l'ip dell'altro giocatore: ")
ipH = input("Inserire il proprio ip: ")
clear = lambda: os.system('cls')
clear()
client = myThread("Thread_Client", ipG)
client.start()
server = myThread("Thread_Server", ipH)
server.start()
