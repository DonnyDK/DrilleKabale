import os
import socket
import pickle
import time

SERVER_IP = '192.168.1.100'
PORT = 5659
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'Disconnected!'

name = str(input('Name? '))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

client.send(name.encode(FORMAT))
ID = client.recv(1024).decode(FORMAT)
while True:

    client.send('get'.encode(FORMAT))
    table = pickle.loads(client.recv(16384))
    player = table.players[ID]
    if table:
        os.system('cls')
        print(f'Your player name: {name}\n')
        table.showFields()
        print('-----------------------------------------------------------')
        names, stacks = table.show_stacks()
        for i, j in enumerate(names):
            if not j == name:
                print(f'{j}´s stack top card: {stacks[i]}')

        if player.hasTurn:
            table.draw(player, 5)
            print(player.showHand())


        print(ID)

        data = input('say something: ')
