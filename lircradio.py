import socket
import lirc
import os

class Stream:

    def __init__(self, channel, name, url, genre):
        self.genre = genre
        self.channel = channel
        self.name = name
        self.url = url

    def getName(self):
        return self.name

    def getChannel(self):
        return self.channel

    def getURL(self):
        return self.url

    def getGenre(self):
        return self.genre

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
   

    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((addr, port))

    def shutdown(self):
        self.socket.send('quit\n'.encode('utf-8'))
        self.socket.close()
    
    def send(self, command):
        self.socket.send((command + '\n').encode('utf-8'))

class IRInterface:

    def __init__(self):
        lirc.init("lircradiosystem","lircradiosystem.lirc")
        self.counter = 3
        self.channel = ""
        self.numkeys = ["key-zero","key-one","key-two","key-three","key-four","key-five","key-six","key-seven","key-eight","key-nine"]
        
    def readIRInput(self):
        i = lirc.nextcode()
        if len(i)>0:
            command = i[0]
            for i, j in enumerate(self.numkeys):
                if j == command:
                    self.channel = self.channel+str(i)
                    self.counter = self.counter - 1
                    if self.counter == 0:
                        result = "key-channelselection " + self.channel
                        self.channel = ""
                        self.counter = 3
                        return result
                    else:
                        return ""
            return command
        return ""

class MainRadioSystem:

    def __init__(self):
        self.v = None
        self.streamlist = []
        self.genrelist = []
        self.currentgenreindex = 0
        self.currentstreamindex = 0
        self.previousstreamindex = 0

    def readStreamList(self):
        f = open('streams.txt', 'r')
        lines = f.readlines()
        for line in lines:
            s = line.split(',')
            genre = s[3].split('\n')[0]
            if not genre in self.genrelist:
                self.genrelist.append(genre)
            self.streamlist.append(Stream(int(s[0]), s[1], s[2], genre))
        self.streamlist.sort(key=lambda x: x.getChannel(), reverse=False)
        self.genrelist.sort()
        f.close()
       
    def shutdown(self):
        self.v.shutdown()
        lirc.deinit()
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
        self.v.send(self.v.VOLUP + ' 1')

    def voldown(self):
        self.v.send(self.v.VOLDOWN + ' 1')           

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

    def mainLoop(self):
        self.v = VLCInterface("localhost", 8080)
        print("Connected")
        irint = IRInterface()
        print("IR interface loaded")
        self.readStreamList()
        print("Stream file read")

        print("Starting loop")
        while True:
            try:
                i = irint.readIRInput()
                if len(i) > 0:
                    self.processIRInput(i)
            except (KeyboardInterrupt):
                self.shutdown()
                print("Shutting down")

if __name__ == "__main__":
    m = MainRadioSystem()
    m.mainLoop()
