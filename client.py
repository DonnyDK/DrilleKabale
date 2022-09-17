import os
import socket
import pickle
import time
import settings
import sys

name = None
SERVER_IP = None
try:
    SERVER_IP = sys.argv[1]
except IndexError:
    pass

if not SERVER_IP:
    SERVER_IP = str(input('Enter servers ip: '))

if not SERVER_IP:
    SERVER_IP = settings.SERVER_IP

try:
    name = sys.argv[2]
except IndexError as e:
    print(e)

if not name:
    name = str(input('Enter Name: '))

if not name:
    name = settings.name


PORT = 5660
ADDR = (SERVER_IP, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = 'Disconnected!'
LINE = '-----------------------------------------------------------'

source, scr, dest, augment = 0,0,0,0

def secure_input(msg):
    while True:
        try:
            move = input(msg)
            move = int(move)
            return move
        except ValueError:
            print('Please input a number ')


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

client.send(name.encode(FORMAT))
ID = int(client.recv(1024).decode(FORMAT))
while True:
    source, scr, dest, augment = 0, 0, 0, 0
    get = 'get'
    client.send(pickle.dumps(get))
    table = pickle.loads(client.recv(16384))
    player = table.players[ID]

    if table:
        if table.running:
            os.system('cls')
            print(f'Your player name: {name} ID: {ID}\n')
            table.showFields()
            print(LINE)
            names, stacks = table.show_stacks(name)
            for i, j in enumerate(names):
                if not j == name:
                    print(f'{j}´s stack: {stacks[i]}')
            print(f'\nYour stack: {player.showStack()} ({len(player.stack)}) | Jokers: {player.showJoker()} | '
                  f'Buffers {player.showBuffer(1)} ({len(player.buffer[0])}) {player.showBuffer(2)} ({len(player.buffer[1])}) '
                  f'{player.showBuffer(3)} ({len(player.buffer[2])})')
            print(LINE)


            if player.hasTurn:
                print(f'Your Hand: {player.showHand()}\n')

                ### Playing

                # Choose where to play from
                playSource = ['1 = hand', '2 = joker', '3 = buffer', '4 = stack']
                source = secure_input(f'Where do you want to play from? ({playSource[0]} {playSource[1]} {playSource[2]} {playSource[3]}): ')

                # Play from hand
                if source == 1:
                    scr = secure_input(f'What card do you wanna play? (1-{len(player.hand)}): ')
                    hand_dest = ['1 = table stack', '2 = other players stack', '3 = buffer']
                    dest = secure_input(f'Where do you want to play to? ({hand_dest[0]} {hand_dest[1]} {hand_dest[2]}) ')

                    if dest == 1:
                        augment = secure_input(f'What field? (1 - {len(table.fields)})')
                    if dest == 2:
                        augment = input(f'What player? (enter player name.)')
                    if dest == 3:
                        augment = input('What buffer? (1-3)')

                # Play from Joker
                if source == 2:
                    dest = 0
                    augment = secure_input(f'What field? (1 - {len(table.fields)})')

                #Play from buffer
                if source == 3:
                    dest = input('What buffer? (1-3)')
                    augment = secure_input(f'What field? (1 - {len(table.fields)})')

                # Play from stack
                if source == 4:
                    stack_dest = ['1 = table stack', '2 = other players stack']
                    dest = secure_input(f'Where do you want to play to? ({stack_dest[0]} {stack_dest[1]}) ')

                    if dest == 1:
                        augment = secure_input(f'What field? (1 - {len(table.fields)})')

                    if dest == 2:
                        augment = input(f'What player? (enter player name.)')

                data = source, scr, dest, augment, ID
                client.send(pickle.dumps(data))

            else:
                time.sleep(1)

    else:
        print('\nA player disconnected. Shutting down')
        time.sleep(2)
        exit()



