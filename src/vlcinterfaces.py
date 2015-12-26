import socket, subprocess, time
from src.configs import Config
#import configs.Config

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
   

    def __init__(self):
        self.vol = 200
        self.oldvol = -1
        #Remove this line:
        Config("../default.conf")
        if Config.isloaded:
            self.addr = Config.configDict["RC_HOST"].split(":")[0]
            self.port = int(Config.configDict["RC_HOST"].split(":")[1])
        else:
            print("Error: VLCInterface: Config file has not been loaded.")
            exit(1)

        runcommand = []
        if Config.configDict["VLC"]:
            runcommand.append(Config.configDict["VLC"])
        if Config.configDict["RC_HOST"]:
            runcommand.append("--extraintf")
            runcommand.append("rc")
            runcommand.append("--rc-host")
            runcommand.append(Config.configDict["RC_HOST"])
        if Config.configDict["HTTP_ENABLED"] == "1":
            runcommand.append("-I")
            runcommand.append("http") 
            if Config.configDict["HTTP_SRC"]:
                runcommand.append("--http-src")
                runcommand.append(Config.configDict["HTTP_SRC"])
            if Config.configDict["HTTP_PASSWORD"]:
                runcommand.append("--http-password")
                runcommand.append(Config.configDict["HTTP_PASSWORD"])
            if Config.configDict["HTTP_HOST"]:
                runcommand.append("--http-host")
                runcommand.append(Config.configDict["HTTP_HOST"])
            if Config.configDict["HTTP_PORT"]:
                runcommand.append("--http-port")
                runcommand.append(Config.configDict["HTTP_PORT"])
        print("Starting the player with the following command: \n\t"+" ".join(runcommand))    
        self.process = subprocess.Popen(runcommand)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tries = 10
        while tries > 0:
            try:
                self.socket.connect((self.addr, self.port))
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
    
    def play(self):
        self.send(self.PLAY)

    def stop(self):
        self.send(self.STOP)

    def pause(self):
        self.send(self.PAUSE)
        
    def volup(self, amount):
        self.oldvol = self.vol
        self.vol = self.vol + amount
        self.send(self.VOLUME + ' ' + str(self.vol))

    def voldown(self, amount):
        self.oldvol = self.vol
        self.vol = self.vol - amount
        self.send(self.VOLUME + ' ' + str(self.vol))
        
    def volume(self, volume):
        self.oldvol = self.vol
        self.vol = volume
        self.send(self.VOLUME + ' ' + str(volume))

    def clear(self):
        self.send(self.CLEAR)
    
    def play(self, url):
        self.send(self.CLEAR)
        self.send(self.ADD + " " + url)

    def mute_unmute(self):
        if self.vol == 0:
            self.vol = self.oldvol
            self.send(self.VOLUME + ' ' + str(self.vol))
        else:
            self.oldvol = self.vol
            self.vol = 0
            self.send(self.VOLUME + ' ' + str(self.vol))
    
    def send(self, command):
        self.socket.send((command + '\n').encode('utf-8'))

if __name__ == "__main__":
    v = VLCInterface()