import json
import urllib2
from xml.dom import minidom

class AbstractSongReader(object):

    def read(self):
        raise NotImplementedError("You cannot run an abstract class!")
    
class VLCSongReader(AbstractSongReader):

    def __init__(self):
        self.req = urllib2.Request('http://localhost:8080/now_playing_raw.xml')

    def read(self):
        resp = urllib2.urlopen(self.req)
        content = resp.read()
        return content.replace("\n", "")

class SkyradioReader(AbstractSongReader):
    
    def __init__(self):
        self.req = urllib2.Request('http://www.skyradio.nl/cdn/player_skyradio.xml')

    def read(self):
        resp = urllib2.urlopen(self.req)
        content = resp.read()
        xmldoc = minidom.parseString(content)
        attributes = xmldoc.getElementsByTagName('attribute')
        title = ""
        artist = ""
        for attribute in attributes:
            if attribute.attributes["name"].value=="cue_title":
                title = attribute.firstChild.data
            if attribute.attributes["name"].value=="track_artist_name":
                artist = attribute.firstChild.data
        return artist + " - " + title
                

class Radio4SongReader(AbstractSongReader):

    def __init__(self):
        self.req = urllib2.Request('http://www.radio4.nl/data/nowplaying.json')

    def read(self):
        resp = urllib2.urlopen(self.req)
        content = resp.read()
        jsondoc = json.loads(content)
        return jsondoc["song"]["composer"] + " - " + jsondoc["song"]["title"]

class Radio2SongReader(AbstractSongReader):

    def __init__(self):
        self.req = urllib2.Request('http://radiobox2.omroep.nl/data/radiobox2/nowonair/2.json')

    def read(self):
        resp = urllib2.urlopen(self.req)
        content = resp.read()
        jsondoc = json.loads(content)
        return jsondoc["results"][0]["songfile"]["artist"] + " - " + jsondoc["results"][0]["songfile"]["title"]


if __name__ == "__main__":
    print(SkyradioReader().read())
