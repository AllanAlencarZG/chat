import socket
import struct
import PySimpleGUI as sg
from threading import Thread

from time import sleep
def listenServer():
    while True:
        size_data = b''
        while len(size_data) < 4:
            size_data += sock.recv(4 - len(size_data))
        size_data = struct.unpack('!I', size_data)[0]
        
        data = b''
        while len(data) < size_data:
            data += sock.recv(size_data - len(data))
        print(data.decode(encoding="utf-8"))

def sendText(msg='', nickname=''):
    msg = f'{nickname if len(nickname) > 0 else "anônimo"}: {msg}'
    size_data = struct.pack('!I', len(msg))
    sock.sendall(size_data + msg.encode(encoding="utf-8"))

def mainWindow():
    sg.theme('Reddit')

    layout = [
        [sg.Text('Nickname: '), sg.Input(size=(10, 1), key='-nn-')],
        [sg.Output(size=(35, 20), key='-op-',)],
        [sg.Button('Enviar'), sg.Input(size=(25, 1), key='-input-')]
    ]

    window = sg.Window('FK messager', layout=layout, finalize=True)

    window['-input-'].bind("<Return>", "Enter")

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED:
            break
        if event == '-input-Enter' or event == 'Enviar':
            if len(values['-input-']) > 0:
                sendText(msg=str(values['-input-']), nickname=values['-nn-'])
        
if __name__ == '__main__':
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 25357))
            break
        except (socket.error, socket.timeout):
            print('Tentando se conectar ao servidor...')
            sleep(1)
    
    Thread(target=listenServer).start()
    mainWindow()
