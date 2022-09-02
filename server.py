import pickle
import socket
import time
from _thread import *

from deck import Deck
from table import Table
SERVER_IP = '192.168.1.100'
PORT = 5659
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'Disconnected!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

tables = {}
gameId = 0

def handle_connection(conn, addr, gameId, ID):

    print(f'New connection. {addr[0]} connected.')

    connected = True
    while connected:

        if gameId in tables:
            try:
                data = pickle.loads(conn.recv(2048000))

                if not data:
                    break
                else:
                    if data == 'get':
                        conn.sendall(pickle.dumps(tables[gameId]))
                        print('sending table')

                    else:
                        print('recived Data', ID)
                        print(data)
                        tables[gameId].move(ID, data)


            except EOFError as e:
                print(e)
                time.sleep(1)




def start():
    global gameId
    count = 1
    #choice = 2
    choice = int(input('How many players are connecting? '))
    print(f'Server address: {SERVER_IP}')
    player_names = []
    server.listen(choice)
    print('Server started. Waiting for players to connect.')

    waiting = True
    while waiting:
        conn, addr = server.accept()
        player_name = conn.recv(1024).decode(FORMAT)
        ID = addr[1]
        print(type(ID))
        player_names.append((player_name, ID))
        conn.send(str(ID).encode(FORMAT))
        print(f'player named {player_name} added to the game.')
        start_new_thread(handle_connection, (conn, addr, gameId, ID))
        #time.sleep(0.1)

        if len(player_names):

            tables[gameId] = Table(player_names, Deck(choice))
            print('Starting game!')
            #table.players[random.random()]
            tables[gameId].running = True
            for player in tables[gameId].players:
                if tables[gameId].players[player].hasTurn:
                    tables[gameId].draw(player, 5)
            gameId += 1
            waiting = False




start()
while True:
   pass
