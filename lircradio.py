import socket
import os
import sys
import threading
import src.vlcinterfaces
import src.irinterfaces
import src.streams
import src.configs
import src.logger

class MainRadioSystem:

    def __init__(self):
        self.v = None
        self.streamlist = list()
        self.genrelist = list()
        self.currentgenreindex = 0
        self.currentstreamindex = 0
        self.previousstreamindex = 0
        self.channelmapping = dict()
        self.irint = None

    def readSourceStreamList(self):
        #print(os.getcwd())
        src.logger.logInfo("Reading streams source file...")
        if os.path.isfile(src.configs.Config.configDict["STREAM_SOURCE_FILE"]):
            f = open(src.configs.Config.configDict["STREAM_SOURCE_FILE"], 'r')
            lines = f.read().split('\n')
            for line in lines:
                if not line:
                    continue
                s = line.split(',')
                genre = s[3]
                if not genre in self.genrelist:
                    self.genrelist.append(genre)
                self.streamlist.append(src.streams.Stream(int(s[0]), s[1], s[2], genre))
            self.streamlist.sort(key=lambda x: x.getChannel(), reverse=False)
            self.genrelist.sort()
            f.close()
        else:
            src.logger.logFError("Error: No streams have been loaded because the streams.source was not found.")
            self.shutdown()
        src.logger.logOk("Streams source file read.")
            
    def readSelectionStreamList(self):
        if not os.path.isfile(src.configs.Config.configDict["STREAM_SELECTION_FILE"]):
            f = open(src.configs.Config.configDict["STREAM_SELECTION_FILE"],'w')
            f.write("\n")
            f.close()
        f = open(src.configs.Config.configDict["STREAM_SELECTION_FILE"],'r')
        lines = f.read().split('\n')
        for line in lines():
            if not line:
                continue
            s = line.split('=')
            selchannel = s[0]
            srcchannel = s[1]
            self.channelmapping[selchannel]=srcchannel
        f.close()
        
    def saveSelectionStreamList(self):
        out = ""
        for key in self.channelmapping.keys():
            out = out + key + "=" + self.channelmapping[key] + "\n"
        f = open(src.configs.Config.configDict["STREAM_SELECTION_FILE"],'w')
        f.write(out)
        f.close()
       
    def shutdown(self):
        src.logger.logInfo("Shutting down radio...")
        self.v.shutdown()
        self.irint.shutdown()
        #os.system("shutdown now -h")
        exit(0)

    def previousChannel(self):
        self.playstreamindex(self.previousstreamindex)

    def nextGenre(self):
        index = self.currentgenreindex + 1
        while index >= len(self.genrelist):
            index = index - len(self.genrelist)
        src.logger.logInfo("Picking genre: " + self.genrelist[index])
        for i in range(0, len(self.streamlist)):
            if self.streamlist[i].getGenre()==self.genrelist[index]:
                self.playstreamindex(i)
                return

    def previousGenre(self):
        index = self.currentgenreindex - 1
        while index < 0:
            index = index + len(self.genrelist)
        src.logger.logInfo("Picking genre: " + self.genrelist[index])
        for i in range(0, len(self.streamlist)):
            if self.streamlist[i].getGenre()==self.genrelist[index]:
                self.playstreamindex(i)
                return

    def nextStreamInGenre(self):
        for i in range(self.currentstreamindex+1, len(self.streamlist)):
            if self.streamlist[i].getGenre()==self.genrelist[self.currentgenreindex]:
                self.playstreamindex(i)
                return
        for i in range(0, self.currentstreamindex+1):
            if self.streamlist[i].getGenre()==self.genrelist[self.currentgenreindex]:
                self.playstreamindex(i)
                return

    def previousStreamInGenre(self):
        for i in range(self.currentstreamindex-1, -1, -1):
            if self.streamlist[i].getGenre()==self.genrelist[self.currentgenreindex]:
                self.playstreamindex(i)
                return
        for i in range(len(self.streamlist), self.currentstreamindex-1, -1):
            if self.streamlist[i].getGenre()==self.genrelist[self.currentgenreindex]:
                self.playstreamindex(i)
                return

    def findIndexForNearestPreviousChannel(self, channelnumber):
        result = 0
        for i in range(0, len(self.streamlist)):
            channel = self.streamlist[i].getChannel()
            if channel == channelnumber:
                self.playstreamindex(i)
                return
            if channel < channelnumber:
                if channel > result:
                    result = i

        self.playstreamindex(result)

    def nextStream(self):
        index = self.currentstreamindex + 1
        while index >= len(self.streamlist):
            index = index - len(self.streamlist)
        self.playstreamindex(index)

    def previousStream(self):
        index = self.currentstreamindex - 1
        while index < 0:
            index = index + len(self.streamlist)
        self.playstreamindex(index)

    def playstreamindex(self, index):
        src.logger.logInfo("Playing: " + self.streamlist[index].getURL())
        self.v.play(self.streamlist[index].getURL())
        self.previousstreamindex = self.currentstreamindex
        self.currentstreamindex = index
        self.currentgenreindex = self.genrelist.index(self.streamlist[index].getGenre())

    def processIRInput(self, i):
        src.logger.logInfo("Received input: " + i)
        if "key-channelselection" in i:
            channel = int(i.split(' ')[1])
            self.findIndexForNearestPreviousChannel(channel)
        elif "key-play" in i:
            self.v.play()
        elif "key-quit" in i:
            self.shutdown()
        elif "key-pause" in i:
            self.v.pause()
        elif "key-stop" in i:
            self.v.stop()
        elif "key-next" in i:
            self.nextStream()
        elif "key-prev" in i:
            self.previousStream()
        elif "key-nextgenre" in i:
            self.nextGenre()
        elif "key-previousgenre" in i:
            self.previousGenre()
        elif "key-volup" in i:
            self.v.volup(5)
        elif "key-voldown" in i:
            self.v.voldown(5)
        elif "key-previouschannel" in i:
            self.previousChannel()
        elif "key-mute" in i:
            self.v.mute_unmute()

    def extractConfigFileArgument(self):
        if len(sys.argv) > 1:
            return sys.arv[1]
        return ""
    
    def readLoop(self):
        src.logger.logInfo("Waiting for IR input...")
        while True:
            try:
                i = self.irint.readIRInput()
                if len(i) > 0:
                    self.processIRInput(i)
            except (KeyboardInterrupt):
                src.logger.logInfo("Exiting main loop...")
                self.shutdown()
    
    def mainLoop(self):
        cfile = "default.conf"
        if self.extractConfigFileArgument():
            cfile = self.extractConfigFileArgument()
        src.configs.Config(cfile)
           
        self.readSourceStreamList()
                 
        self.v = src.vlcinterfaces.VLCInterface()
        self.v.volume(self.v.vol)
        self.irint = src.irinterfaces.IRInterface()


        src.logger.logInfo("Starting main loop...")
        self.readLoop()
        #t=threading.Thread(target=self.readLoop)
        #t.daemon = True
        #t.start()
                

if __name__ == "__main__":
    m = MainRadioSystem()
    m.mainLoop()
