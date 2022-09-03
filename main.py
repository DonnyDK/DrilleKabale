from client import client
from server import server

def main_network():
    start = input(f'What to start? (1 = client | 2 = server): ')

    if start == 1:
        client()
    elif start == 2:
        server()

main_network()