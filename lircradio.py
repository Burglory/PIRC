import socket
import os
import src.vlcinterfaces
import src.irinterfaces
import src.streams






class MainRadioSystem:

    def __init__(self):
        self.v = None
        self.streamlist = list()
        self.genrelist = list()
        self.currentgenreindex = 0
        self.currentstreamindex = 0
        self.previousstreamindex = 0
        self.volume = 200
        self.oldvolume = -1
        self.channelmapping = dict()
        self.irint = None

    def readSourceStreamList(self):
        f = open('streams.source', 'r')
        lines = f.readlines()
        for line in lines:
            s = line.split(',')
            genre = s[3].split('\n')[0]
            if not genre in self.genrelist:
                self.genrelist.append(genre)
            self.streamlist.append(src.streams.Stream(int(s[0]), s[1], s[2], genre))
        self.streamlist.sort(key=lambda x: x.getChannel(), reverse=False)
        self.genrelist.sort()
        f.close()
        
    def readSelectionStreamList(self):
        if not os.path.isfile("streams.selection"):
            f = open('streams.selection','w')
            f.write("\n")
            f.close()
        f = open('streams.selection','r')
        lines = f.readlines()
        for line in lines():
            s = line.split(',')
            selchannel = s[0]
            srcchannel = s[1].replace('\n','')
            self.channelmapping[selchannel]=srcchannel
        f.close()
            
       
    def shutdown(self):
        self.v.shutdown()
        self.irint.shutdown()
        os.system("shutdown now -h")
        exit(0)

    def previousChannel(self):
        self.playstreamindex(self.previousstreamindex)

    def nextGenre(self):
        index = self.currentgenreindex + 1
        while index >= len(self.genrelist):
            index = index - len(self.genrelist)
        print("Picking genre: " + self.genrelist[index])
        for i in range(0, len(self.streamlist)):
            if self.streamlist[i].getGenre()==self.genrelist[index]:
                self.playstreamindex(i)
                return

    def previousGenre(self):
        index = self.currentgenreindex - 1
        while index < 0:
            index = index + len(self.genrelist)
        print("Picking genre: " + self.genrelist[index])
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
        print("Enqueueing: " + self.streamlist[index].getURL())
        #self.v.send(self.v.ENQUEUE + ' ' + self.streamlist[index].getURL())
        #self.v.send(self.v.NEXT)
        self.v.send(self.v.CLEAR)
        self.v.send(self.v.ADD + ' ' + self.streamlist[index].getURL())
        self.previousstreamindex = self.currentstreamindex
        self.currentstreamindex = index
        self.currentgenreindex = self.genrelist.index(self.streamlist[index].getGenre())

    def play(self):
        self.v.send(self.v.PLAY)

    def stop(self):
        self.v.send(self.v.STOP)

    def pause(self):
        self.v.send(self.v.PAUSE)

    def volup(self):
        self.oldvolume = self.volume
        self.volume = self.volume + 5
        self.v.send(self.v.VOLUME + ' ' + str(self.volume))

    def voldown(self):
        self.oldvolume = self.volume
        self.volume = self.volume - 5
        self.v.send(self.v.VOLUME + ' ' + str(self.volume))

    def mute_unmute(self):
        if self.volume == 0:
            self.volume = self.oldvolume
            self.v.send(self.v.VOLUME + ' ' + str(self.volume))
        else:
            self.oldvolume = self.volume
            self.volume = 0
            self.v.send(self.v.VOLUME + ' ' + str(self.volume))

    def processIRInput(self, i):
        print("received input: " + i)
        if "key-channelselection" in i:
            channel = int(i.split(' ')[1])
            self.findIndexForNearestPreviousChannel(channel)
        elif "key-play" in i:
            self.play()
        elif "key-quit" in i:
            self.shutdown()
        elif "key-pause" in i:
            self.pause()
        elif "key-stop" in i:
            self.stop()
        elif "key-next" in i:
            self.nextStream()
        elif "key-prev" in i:
            self.previousStream()
        elif "key-nextgenre" in i:
            self.nextGenre()
        elif "key-previousgenre" in i:
            self.previousGenre()
        elif "key-volup" in i:
            self.volup()
        elif "key-voldown" in i:
            self.voldown()
        elif "key-previouschannel" in i:
            self.previousChannel()
        elif "key-mute" in i:
            self.mute_unmute()


    
    def mainLoop(self):
        self.v = src.vlcinterfaces.VLCInterface("localhost", 8080)
        self.v.send(self.v.VOLUME + ' ' + str(self.volume))
        print("Connected")
        self.irint = src.irinterfaces.IRInterface()
        print("IR interface loaded")
        self.readSourceStreamList()
        print("Stream file read")

        print("Starting loop")
        while True:
            try:
                i = self.irint.readIRInput()
                if len(i) > 0:
                    self.processIRInput(i)
            except (KeyboardInterrupt):
                self.shutdown()
                print("Shutting down")

if __name__ == "__main__":
    m = MainRadioSystem()
    m.mainLoop()
