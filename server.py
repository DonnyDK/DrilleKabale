import pickle
import socket
import threading
from deck import Deck
from table import Table

IP_CHECK = input(f'Press enter if your ip is {socket.gethostbyname(socket.gethostname())}, or type your ip, followed by hitting enter: ')

if IP_CHECK:
    SERVER_IP = IP_CHECK
else:
    SERVER_IP = socket.gethostbyname(socket.gethostname())

PORT = 5660
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'Disconnected!'
LINE = '-----------------------------------------------------------'


tables = {}
gameId = 0

def handle_connection(conn, addr, gameId, ID):
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
                    else:
                        tables[gameId].move(ID, data)
            except EOFError as e:
                print(tables[gameId].players[ID].name, DISCONNECT_MSG)
                tables[gameId].running = False
                break


def server():
    global gameId
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    count = 1
    choice = int(input('How many players are connecting? '))
    #choice = 2
    print(f'Server address: {SERVER_IP}')
    player_names = []
    server.listen(choice)
    print('Server started. Waiting for players to connect.')
    print(LINE)

    waiting = True
    while True:
        while waiting:
            conn, addr = server.accept()
            player_name = conn.recv(1024).decode(FORMAT)
            ID = addr[1]

            player_names.append((player_name, ID))
            conn.send(str(ID).encode(FORMAT))
            print(f'New connection.{player_name} connected from {addr[0]}.')
            print(LINE)
            threading.Thread(target=handle_connection, args=(conn, addr, gameId, ID)).start()
            #time.sleep(0.1)

            if len(player_names) == choice:

                tables[gameId] = Table(player_names, Deck(choice))
                print('Starting game!')
                tables[gameId].running = True

                for player in tables[gameId].players:
                    if tables[gameId].players[player].hasTurn:
                        tables[gameId].draw(tables[gameId].players[player].id, 5)

                tables[gameId].ides()
                gameId += 1
                waiting = False

            print(threading.active_count())

        if threading.active_count() == 1:
            break



server()
