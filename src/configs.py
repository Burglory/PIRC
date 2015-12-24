import os.path

class Config(object):

    configDict = dict()
    file_path = None

    def __init__(self, file_path):
        Config.configDict = dict()
        self.load(file_path)
        Config.file_path = file_path

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
            Config.configDict[keyvalue[0]] = keyvalue[1]
        print("Config file loaded.")
        Config.file_path = file_path

    def getValue(self, key):
        result = ""
        if key in Config.configDict.keys():
            result = Config.configDict[key]
        return result

    def setValue(self, key, value):
        Config.configDict[key] = value

    def save(self):
        result = ""
        for key in Config.configDict.keys():
            result = result + key + "=" + Config.configDict[key] + "\n"
        f = open(Config.file_path, 'w')
        f.write(result)
        f.close()

if __name__ == "__main__":
    Config("../default.conf")
