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
