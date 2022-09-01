import os
import socket
import pickle
import time

SERVER_IP = '192.168.1.100'
PORT = 5659
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'Disconnected!'
LINE = '-----------------------------------------------------------'
WM = 'Wrong Move!!!'
ADD = 'Added'

name = str(input('Name? '))
print('Connecting to: ', SERVER_IP)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

client.send(name.encode(FORMAT))
ID = client.recv(1024).decode(FORMAT)


def secure_input(msg):
    while True:
        try:
            move = input(msg)

            move = int(move)
            return move
        except ValueError:
            print('Please input a number ')

while True:

    client.send('get'.encode(FORMAT))
    table = pickle.loads(client.recv(16384))
    player = table.players[ID]
    if table:
        os.system('cls')
        print(f'Your player name: {name}\n')
        table.showFields()
        print(LINE)

        names, stacks = table.show_stacks(name)
        for i, j in enumerate(names):
            if not j == name:
                print(f'{j}´s stack: {stacks[i]}')
        print(f'\nYour stack: {player.showStack()} ({len(player.stack)}) | Jokers: {player.showJoker()} | '
              f'Buffers {player.buffer[0]} ({len(player.buffer[0])}) {player.buffer[1]} ({len(player.buffer[1])}) '
              f'{player.buffer[2]} ({len(player.buffer[2])})')
        print(LINE)

        if player.hasTurn:
            table.draw(player, 5)

        if player.hand:
            print(f'Your Hand: {player.showHand()}')

            ### Playing

            # Choose where to play from
            # Players move

            playSource = ['1 = hand', '2 = joker', '3 = buffer', '4 = stack']
            source = secure_input(f'Where do you want to play from? ({playSource[0]} {playSource[1]} {playSource[2]} {playSource[3]}): ')

            if source == 1:
                scr = secure_input(f'What card do you wanna play? (1-{len(player.hand)}): ')
                hand_dest = ['1 = table stack', '2 = other players stack', '3 = buffer']
                dest = secure_input(f'Where do you want to play to? ({hand_dest[0]} {hand_dest[1]} {hand_dest[2]}) ')

                if dest == 1:
                    field = secure_input(f'What field? (1 - {len(table.fields)})')
                    table.move()






        data = input('Press enter to continue')
        client.sendall(pickle.dumps(table))
