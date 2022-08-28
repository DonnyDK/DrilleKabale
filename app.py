from table import Table
from deck import Deck
import os

def setup():
    names = []

    while True:
        try:
            choice = input('How many players? ')
            choice = int(choice)
            break
        except ValueError:
            print('Please put in a number!')

    for i in range(choice):
        names.append(input(f'Player {i + 1}´s name: '))

    table = Table(names, Deck(choice))
    os.system('cls')
    return table



def main_cli(run):

    run = True
    table = setup()

    while run:

        for player in table.players:

            # Starts players trun
            player.hasTurn = True
            MOVE = True
            # Player draws cards
            table.draw(player, 5)
            while player.showStack().value > 12:
                player.jokers.append(player.stack.pop())


            while MOVE:
                # Shows other players stacks
                names, stacks = table.show_stacks()
                for i, j in enumerate(names):
                    print(f'{j}´s stack: {stacks[i]}')

                # Shows table fields
                table.showFields()

                # Shows players cards
                print(f'Your stacks top card: {player.showStack()}\n'
                      f'Your jokers: {player.showJoker()}\n'
                      f'Your Buffer {player.buffer[0][-1:]} {player.buffer[1][-1:]} {player.buffer[2][-1:]}\n'
                      f'Your hand: {player.showHand()}')

                # Players move
                playSource = ['1 = hand', '2 = joker', '3 = buffer', '4 = stack']

                while True:
                    try:
                        move = input(f'Where do you want to play from? ({playSource[0]} {playSource[1]} {playSource[2]} {playSource[3]}): ')
                        move = int(move)
                        break
                    except ValueError:
                        print('Please input a number ')

                # play from hand
                if move == 1:
                    choise = input(f'What card do you wanna play? (1-{len(player.hand)}): ')
                    choise = int(choise)
                    card = player.hand.pop(choise - 1)

                    playDest = ['1 = table stack', '2 = other players stack', '3 = buffer']

                    dest = int(input(f'Where do you want to play to? ({playDest[0]} {playDest[1]} {playDest[2]}) '))

                    # Play to table
                    if dest == 1:
                        field = int(input(f'What field? (1 - {len(table.fields)}): '))
                        if table.addToField(field - 1, card):
                            print('Added')
                        else:
                            player.hand.insert(choise - 1, card)

                    # Play to other players stack
                    if dest == 2:

                        field = str(input(f'Who´s stack? (enter player name): '))

                        if table.add_to_player_stack(card, field):

                            print('Added')
                        else:
                            player.hand.insert(choise - 1, card)
                            print('Wrong move!!!')

                    # Play to Buffer
                    if dest == 3:
                        field = int(input(f'What buffer? (1-3)'))
                        player.buffer[field - 1].append(card)
                        MOVE = False

                    if len(player.hand) < 1:
                        table.draw(player, 5)

                # Play joker
                if move == 2:
                    choise = input(f'What field? ')
                    choise = int(choise) - 1
                    card = player.jokers.pop()

                    if table.addToField(choise, card):
                        print('Added')
                    else:
                        print('Wrong Move!!!')
                        player.jokers.append(card)

                # Play from buffer
                if move == 3:
                    choise = input(f'What buffer? (1 - 3)')
                    choise = int(choise) - 1

                    try:
                        card = player.buffer[choise].pop()

                        field = int(input(f'What field? '))

                        if table.addToField(field - 1, card):
                            print('Added')
                        else:
                            print('Wrocg move!!!')
                            player.buffer[choise].append(card)

                    except IndexError:
                        print('Wrong move!!!')

                if move == 4:

                    try:
                        card = player.stack.pop()
                    except IndexError:
                        print('Wrong move!!!')



                    playDest = ['1 = table stack', '2 = other players stack']

                    dest = int(input(f'Where do you want to play to? ({playDest[0]} {playDest[1]}) '))

                    # Play to table
                    if dest == 1:
                        field = int(input(f'What field? (1 - {len(table.fields)}): '))
                        if table.addToField(field - 1, card):
                            print('Added')
                        else:
                            player.hand.insert(choise - 1, card)

                    # Play to other players stack
                    if dest == 2:

                        field = str(input(f'Who´s stack? (enter player name): '))

                        if table.add_to_player_stack(card, field):

                            print('Added')
                        else:
                            player.stack.append(card)
                            print('Wrong move!!!')



                # Ends players turn

                os.system('cls')
                player.hasTurn = False
