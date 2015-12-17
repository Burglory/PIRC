import socket, subprocess, time

class VLCInterface:

    PLAY = 'play'
    STOP = 'stop'
    NEXT = 'next'
    ENQUEUE = 'enqueue'
    PAUSE = 'pause'
    CLEAR = 'clear'
    GOTO = 'goto'
    VOLUP = 'volup'
    VOLDOWN = 'voldown'
    ADD = 'add'
    VOLUME = 'volume'
   

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.process = subprocess.Popen(['cvlc','-I','http','--extraintf','rc','--rc-host','localhost:8080','--http-src','','--http-password','admin','--http-host','localhost:80','--http-port','80','http://icecast.omroep.nl/radio4-bb-mp3'])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tries = 10
        while tries > 0:
            try:
                self.socket.connect((addr, port))
                break
            except ConnectionRefusedError:
                tries = tries - 1
                time.sleep(3)
        if tries == 0:
            print("Error: Failed to create VLCInterface. Connection refused.")
            self.process.kill()

    def shutdown(self):
        self.socket.send('quit\n'.encode('utf-8'))
        self.socket.close()
        self.process.kill()
    
    def send(self, command):
        self.socket.send((command + '\n').encode('utf-8'))
