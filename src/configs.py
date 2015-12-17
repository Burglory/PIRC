import os.path

class Config(object):

    def __init__(self, file_path):
        self.configdictionary = dict()
        self.load(file_path)

    def load(self, file_path):
        f = None
        if os.path.isfile(file_path):
            f = open(file_path, 'r')
        else:
            print("Error: Cannot find config file: " + file_path)
            print("Falling back on default config file.")
            if os.path.isfile('default.conf'):
                f = open('default.conf','r')
            else:
                print("Error: Cannot find config file: default.conf")
                print("Config has not been loaded.")
                return
        contents = f.read()
        f.close()
        lines = contents.split("\n")
        for line in lines:
            keyvalue = line.split("=", 1)
            self.configdictionary[keyvalue[0]] = keyvalue[1]
        print("Config file loaded.")



if __name__ == "__main__":
    Config("../default.conf")
