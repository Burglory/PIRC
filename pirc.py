import socket
import os
import sys
import threading
import argparse
import src.vlcinterfaces
import src.irinterfaces
import src.streams
import src.configs
import src.logger
import src.updater
import src.argumentparser
import src.sessions

class MainRadioSystem:

    def __init__(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
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
            src.logger.logFError("No streams have been loaded because the streams.source was not found.")
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
        src.sessions.save()
        if self.v:
            self.v.shutdown()
        if self.irint:
            self.irint.shutdown()
        #os.system("shutdown now -h")
        src.logger.logOk("Exiting...")
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

    def play(self):
        self.playstreamindex(self.currentstreamindex)

    def playstreamindex(self, index):
        src.logger.logInfo("Playing: " + self.streamlist[index].getURL())
        self.v.play(self.streamlist[index].getURL())
        self.previousstreamindex = self.currentstreamindex
        self.currentstreamindex = index
        self.currentgenreindex = self.genrelist.index(self.streamlist[index].getGenre())
        src.sessions.defaultsession.setLastPlayed(self.currentstreamindex)
    
    def readLoop(self):
        src.logger.logInfo("Waiting for IR input...")
        while True:
            try:
                self.irint.processIRInput()
            except (KeyboardInterrupt):
                src.logger.logInfo("Exiting main loop...")
                self.shutdown()

    def update(self):
        src.updater.update()

    def restart(self):
        args = sys.argv[:]
        if "--update" in args: args.remove("--update")
        if "-U" in args: args.remove("-U")
        
        
        pyfile = args[0].split('/')[-1]

        args.insert(0, sys.executable)
        args.insert(1, pyfile)
        src.logger.logInfo('Re-spawning %s' % ' '.join(args))
        if sys.platform == 'win32':
            args = ['"%s"' % arg for arg in args]

        #os.chdir(os.path.dirname(os.path.realpath(__file__)))
        os.execv(sys.executable, args)
        
    def mainLoop(self):
        src.argumentparser.parse(self, sys.argv[1:])
           
        self.readSourceStreamList()
                 
        self.v = src.vlcinterfaces.VLCInterface()
        self.v.volume(src.sessions.defaultsession.getLastVolume())
        self.playstreamindex(src.sessions.defaultsession.getLastPlayed())
        self.irint = src.irinterfaces.IRInterface(self)


        src.logger.logInfo("Starting main loop...")
        #self.restart()
        self.readLoop()
        #t=threading.Thread(target=self.readLoop)
        #t.daemon = True
        #t.start()
 
                

if __name__ == "__main__":
    m = MainRadioSystem()
    m.mainLoop()
