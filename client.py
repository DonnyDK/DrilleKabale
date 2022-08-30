import socket
import pickle
import time

SERVER_IP = '192.168.1.100'
PORT = 5657
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

    if table:
        table.showFields()

        data = input('say something: ')


        client.send('get'.encode(FORMAT))


