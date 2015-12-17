import urllib2, time, threading

class SongnameGetter:

    def __init__(self):
        self.req = urllib2.Request('http://127.0.0.1:8080/now_playing_raw.xml')
        self.req.add_header('Authorization', 'Basic OmZyYW5r')
        self.name = ""
        self.terminate = False
        self.t = None

    def terminate(self):
        self.terminate = True

    def startThread(self):
        self.t = threading.Thread(target=self.loop)
        self.t.daemon = True
        self.t.start()

    def loop(self):
        while not self.terminate:
            time.sleep(1)
            resp = urllib2.urlopen(self.req)
            content = resp.read()
            self.name = content.replace("\n","")
            print(self.name)

    def getName(self):
        return self.name

if __name__ == "__main__":
    SongnameGetter().startThread()
