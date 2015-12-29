import os
import src.configs
import src.logger

class Session(object):
        
    def __init__(self):
        self.lastplayed=0
        self.lastvolume=int(src.configs.Config.configDict["VOLUME_BASE"])
    
    def setLastPlayed(self, l):
        self.lastplayed = l
    
    def getLastPlayed(self):
        return self.lastplayed
    
    def setLastVolume(self, v):
        self.lastvolume = v
        
    def getLastVolume(self):
        return self.lastvolume

def save():
    saveToFile(src.configs.Config.configDict["SESSION_FILE"])
    
def saveToFile(file_path):
    f = open(file_path, 'w')
    result = ""
    result = result + "LASTPLAYED" + "="+str(defaultsession.getLastPlayed())+"\n"
    result = result + "LASTVOLUME" + "="+str(defaultsession.getLastVolume())+"\n"
    f.write(result)
    f.close()

def load():
    return loadFromFile(src.configs.Config.configDict["SESSION_FILE"])

def loadFromFile(file_path):
    if os.path.isfile(file_path):
        f = open(file_path, 'r')
        string = f.read()
        f.close()
        return loadFromString(string)
    else:
        src.logger.logError("Could not open session file. File does not exist.")
        
def loadFromString(string):
    result = Session()
    lines = string.split('\n')
    for line in lines:
        if not line:
            continue
        if line[0]=='#':
            continue
        linesections = line.split('=', 1)
        if linesections[0]=="LASTPLAYED":
            result.setLastPlayed(int(linesections[1]))
        elif linesections[0]=="LASTVOLUME":
            result.setLastVolume(int(linesections[1]))
    return result

defaultsession=load()
            
        