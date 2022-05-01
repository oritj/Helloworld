import socket
import threading
from threading import Thread, Lock
import time

no_pair_clients = []
paired_clients_X = []
paired_clients_O = []
choosing_clients = []

IP = socket.gethostbyname(socket.gethostname())
PORT = 8820
ADDR = (IP, PORT)
SIZE = 1024
FORMAT = "utf-8"
DISCONNECT_MSG = "!DISCONNECT"

def handle_client (connection, address):
    print(f"[NEW CONNECTION] {address} connected")
    
    connected = True
    while connected:
        msg = connection.recv(SIZE).decode(FORMAT)
        print(f"[{ADDR}] {msg}")
        if msg == DISCONNECT_MSG:  #edit
            connected = False
            break
        if msg == "DONE":
            for i in range (len(paired_clients_X)):
                if (paired_clients_X[i] == (connection, address)):
                    no_pair_clients.append(paired_clients_X[i])
                    choosing_clients.append(paired_clients_O[i])
                    paired_clients_O.remove(paired_clients_O[i])
                    paired_clients_X.remove(paired_clients_X[i])
                        
                elif (paired_clients_O[i] == (connection, address)):
                    choosing_clients.append(paired_clients_X[i])
                    no_pair_clients.append(paired_clients_O[i])
                    paired_clients_O.remove(paired_clients_O[i])
                    paired_clients_X.remove(paired_clients_X[i])
            for i in range(len(choosing_clients)):
                if (choosing_clients[i] == (connection, address)):
                    no_pair_clients.append(choosing_clients[i])
                    choosing_clients.remove(choosing_clients[i])
        elif msg != "":    
            for i in range (len(paired_clients_X)):
                if (paired_clients_X[i] == (connection, address)):
                    send_to_client(paired_clients_O[i][0], msg)
                elif (paired_clients_O[i] == (connection, address)):
                    send_to_client(paired_clients_X[i][0], msg)
    connection.close()

def handle_lists ():
    print("thread running")
    while True:         
        if (len(no_pair_clients) >= 2):
            paired_clients_X.append(no_pair_clients[1])
            paired_clients_O.append(no_pair_clients[0])
            no_pair_clients[1][0].send("X".encode(FORMAT))
            no_pair_clients[0][0].send("O".encode(FORMAT))
            print("new pair, messages sent")
            no_pair_clients.remove(no_pair_clients[1])
            no_pair_clients.remove(no_pair_clients[0])

def send_to_client(connection, msg):
    connection.send(msg.encode(FORMAT))

def main ():
    print ("[STARTING] server is starting...")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    server.listen()
    print (f"[LISTENING] server started succesfuly! now listening on {IP}:{PORT}")
    
    thread = Thread(target = handle_lists, args = ())
    thread.start()
    
    while True:
        connection, address = server.accept()
        thread = Thread(target = handle_client, args = (connection, address))
        thread.start()
        connected = threading.activeCount() 
        print(f"[ACTIVE CONNECTION] {(connected -2)}")
        no_pair_clients.append((connection, address))


if __name__ == "__main__":
    main()