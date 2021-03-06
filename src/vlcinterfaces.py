import socket, subprocess, time
import src.configs
import src.logger
import src.sessions

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
        src.logger.logInfo("Initializing VLCInterface...")
        self.vol = int(src.configs.Config.configDict["VOLUME_BASE"])
        self.oldvol = -1
        self.addr = src.configs.Config.configDict["RC_HOST"].split(":")[0]
        self.port = int(src.configs.Config.configDict["RC_HOST"].split(":")[1])

        runcommand = []
        if src.configs.Config.configDict["VLC"]:
            runcommand.append(src.configs.Config.configDict["VLC"])
        if src.configs.Config.configDict["RC_HOST"]:
            runcommand.append("--extraintf")
            runcommand.append("rc")
            runcommand.append("--rc-host")
            runcommand.append(src.configs.Config.configDict["RC_HOST"])
        if src.configs.Config.configDict["HTTP_ENABLED"] == "1":
            runcommand.append("-I")
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
        src.logger.logInfo("Starting the player.")
        src.logger.log("Starting VLC with: \n"+" ".join(runcommand))    
        self.process = subprocess.Popen(runcommand, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tries = 10
        time.sleep(2)
        src.logger.logInfo("Trying to connect to VLC...")
        while tries > 0:
            try:
                self.socket.connect((self.addr, self.port))
                break
            except ConnectionRefusedError:
                tries = tries - 1
                src.logger.logError("Failed to connect to VLC. Retrying...("+str(tries)+" tries left)")
                time.sleep(1)
                if self.process.poll():
                    src.logger.logFError("VLC terminated prematurely with exitcode: " + str(self.process.poll()))
                    return
                
        if tries == 0:
            src.logger.logFError("Failed to create VLCInterface. Connection refused.")
            self.process.kill()
            return
        if not self.process.poll():
            src.logger.logOk("Succesfully connected to VLC.")
        src.logger.logOk("VLCInterface initialized.")

    def shutdown(self):
        src.logger.logInfo("Deinitializing VLCInterface...")
        self.socket.send('quit\n'.encode('utf-8'))
        self.socket.close()
        self.process.kill()
        src.logger.logOk("VLCInterface deinitialized.")
    
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
        src.sessions.defaultsession.setLastVolume(self.vol)

    def voldown(self, amount):
        self.oldvol = self.vol
        self.vol = self.vol - amount
        self.send(self.VOLUME + ' ' + str(self.vol))
        src.sessions.defaultsession.setLastVolume(self.vol)
        
    def volume(self, volume):
        self.oldvol = self.vol
        self.vol = volume
        self.send(self.VOLUME + ' ' + str(volume))
        src.sessions.defaultsession.setLastVolume(self.vol)

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
