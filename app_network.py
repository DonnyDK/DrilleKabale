from client import client
from client import secure_input
from server import server

def main_network():
    start = secure_input(f'What to start? (1 = client | 2 = server): ')

    if start == 1:
        client()
    elif start == 2:
        server()