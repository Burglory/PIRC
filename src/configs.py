import os.path
import src.logger

class Config(object):

    configDict = {
                  "SOFTWARE_SOURCE_URL":"https://github.com/Burglory/PIRC",
                  "STREAM_SOURCE_FILE":"streams.source",
                  "STREAM_SELECTION_FILE":".streams.selection",
                  "SHUTDOWN_COMMAND":"shutdown -h now",
                  "RC_HOST":"localhost:8080",
                  "HTTP_ENABLED":"1",
                  "HTTP_SRC":" ",
                  "HTTP_HOST":"localhost:80",
                  "HTTP_PASSWORD":"admin",
                  "HTTP_PORT":"80",
                  "VLC":"cvlc",
                  "LIRC_CONFIG_FILE":".lircradiosystem.lirc",
                  "LIRC_CONFIG_PROGRAM_NAME":"lircradiosystem",
                  "SESSION_FILE":".session",
                  "VOLUME_INCREMENT":"5",
                  "VOLUME_BASE":"200",
                  "LIRCD_CLIENT_COMMAND":"irw"
    }
    
    defaultconfigfilename = "default.conf"
    file_path = defaultconfigfilename
    isloaded = False

    def __init__(self, file_path="default.conf"):
        #Config.configDict = dict()
        self.load(file_path)
        Config.file_path = file_path

    def load(self, file_path):
        src.logger.logInfo("Loading config file...")
        f = None
        if os.path.isfile(file_path):
            f = open(file_path, 'r')
        else:
            src.logger.logError("Cannot find config file: " + file_path + " . Falling back on default config file.")
            if os.path.isfile(Config.defaultconfigfilename):
                f = open(Config.defaultconfigfilename,'r')
            else:
                src.logger.logError("Cannot find config file: default.conf . Config has not been loaded.")
                src.logger.logError("Falling back on programmed defaults.")
                return
        contents = f.read()
        f.close()
        lines = contents.split("\n")
        for line in lines:
            if not line:
                continue
            keyvalue = line.split("=", 1)
            if len(keyvalue) != 2:
                src.logger.logFError("A fatal error occurred in reading the config file. The config file has been corrupted:\n"+line)
                exit(1)
            Config.configDict[keyvalue[0]] = keyvalue[1]
        src.logger.logOk("Config file loaded.")
        Config.file_path = file_path
        Config.isloaded = True

    def getValue(self, key):
        result = ""
        if key in Config.configDict.keys():
            result = Config.configDict[key]
        return result

    def setValue(self, key, value):
        Config.configDict[key] = value

    def save(dic):
        src.logger.logInfo("Saving config to file...")
        result = ""
        l = []
        for key in dic.keys():
            l.append(str(key))
        l.sort()
        for key in l:
            result = result + key + "=" + dic[key] + "\n"
        f=None
        if Config.file_path:
            f = open(Config.file_path, 'w')
        else:
            f = open(Config.defaultconfigfilename, 'w')
        f.write(result)
        f.close()
        src.logger.logOk("Config file saved.")

if __name__ == "__main__":
    Config.save()
