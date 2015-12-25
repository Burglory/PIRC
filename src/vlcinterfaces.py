import socket, subprocess, time
import src.configs.Config

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
   

    def __init__(self, addr = "localhost", port = 8080):
        self.volume = 200
        self.oldvolume = -1
        if src.configs.Config.isloaded:
            self.addr = src.configs.Config.configDict["RC_HOST"].split(":")[0]
            self.port = int(src.configs.Config.configDict["RC_HOST"].split(":")[1])
        else:
            self.addr = addr
            self.port = port
        runcommand = []
        if src.configs.Config.configDict["VLC"]:
            runcommand.append(src.configs.Config.configDict["VLC"])
        if src.configs.Config.configDict["RC_HOST"]:
            runcommand.append("--extraintf")
            runcommand.append("rc")
            runcommand.append("--rc-host")
            runcommand.append(src.configs.Config.configDict["RC_HOST"])
        if src.configs.Config.configDict["HTTP_ENABLED"] == "1":
            runcommand.append("--I")
            runcommand.append("http") 
            if src.configs.Config.configDict["HTTP_SRC"]:
                runcommand.append("--http-src")
                runcommand.append(src.configs.Config.configDict["HTTP_SRC"])
            if src.configs.Config.configDict["HTTP_PASSWORD"]:
                runcommand.append("--http-password")
                runcommand.append(src.configs.Config.configDict["HTTP_PASSWORD"])
            if src.configs.Config.configDict["HTTP_HOST"]:
                runcommand.append("--http-host")
                runcommand.append(src.configs.Config.configDict["HTTP_HOST"])
            if src.configs.Config.configDict["HTTP_PORT"]:
                runcommand.append("--http-port")
                runcommand.append(src.configs.Config.configDict["HTTP_PORT"])
            
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
        self.oldvolume = self.volume
        self.volume = self.volume + amount
        self.send(self.VOLUME + ' ' + str(self.volume))

    def voldown(self, amount):
        self.oldvolume = self.volume
        self.volume = self.volume - amount
        self.send(self.VOLUME + ' ' + str(self.volume))

    def clear(self):
        self.send(self.CLEAR)
    
    def play(self, url):
        self.send(self.CLEAR)
        self.send(self.ADD + " " + url)

    def mute_unmute(self):
        if self.volume == 0:
            self.volume = self.oldvolume
            self.send(self.VOLUME + ' ' + str(self.volume))
        else:
            self.oldvolume = self.volume
            self.volume = 0
            self.send(self.VOLUME + ' ' + str(self.volume))
    
    def send(self, command):
        self.socket.send((command + '\n').encode('utf-8'))

if __name__ == "__main__":
    v = VLCInterface()