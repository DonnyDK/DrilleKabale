from table import Table
from deck import Deck
import socket, pickle
from _thread import *

table = None
SERVER_IP = '192.168.1.100'
PORT = 5657
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'Disconnected!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def move(move):
    pass

def handle_connection(conn, addr):
    global table
    #print(00)
    print(f'New connection. {addr} connected.')

    connected = True
    while connected:
        print(0)
        if table:
            try:
                data = conn.recv(1024).decode(FORMAT)
                print(type(data))
                if not data:
                    break
                else:
                    if data == 'get':
                        conn.sendall(pickle.dumps(table))
                        print(1)
                    else:
                        move(data)
                        print(2)

            except KeyboardInterrupt:
                pass


def start():
    global table, player_names
    count = 1
    choice = int(input('How many players are connecting? '))
    print(f'Server address: {SERVER_IP}')
    player_names = []
    server.listen(choice)
    print('Server started. Waiting for players to connect.')

    waiting = True
    while waiting:
        conn, addr = server.accept()
        player_name = conn.recv(1024).decode(FORMAT)
        player_names.append(player_name)
        conn.send(str(addr[1]).encode(FORMAT))
        print(f'player named {player_name} added to the game.')
        start_new_thread(handle_connection, (conn, addr))


        if len(player_names) == choice and not table:
            table = Table(player_names, Deck(choice))
            print('Starting game!')
            table.running = True
            #waiting = False




start()

