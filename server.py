import socket
from threading import Thread
import struct

def handleClient(client_sock=None, addr=None):
    print(f'Conectado com {addr}')
    while True:
        size_data = b''
        while len(size_data) < 4:
            size_data += client_sock.recv(4 - len(size_data))
        size = struct.unpack('!I', size_data)[0]
        
        data = b''
        while len(data) < size:
            data += client_sock.recv(size - len(data))

        print(f'{addr} Mandou mensagem : {data.decode()}')
        
        sendText(msg=data.decode('utf-8'))
        
def sendText(msg=str):
    size_data = struct.pack('!I', len(msg))
    
    for client_sock in conections:
        client_sock.sendall(size_data + msg.encode('utf-8'))

conections = []

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 25357))

sock.listen()

print('Aguardando...')

while True:
    client_sock, addr = sock.accept()
    
    conections.append(client_sock)
    
    Thread(target=handleClient, args=(client_sock, addr)).start()