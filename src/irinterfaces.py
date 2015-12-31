import time
import src.logger
import src.configs

lircinstalled = True
try:
    import lirc
except ImportError:
    src.logger.logFError("Error: Could not import python lirc package. Is it installed? Please install latest version from: https://pypi.python.org/pypi/python-lirc/")
    lircinstalled = False

class IRInterface(object):

    def __init__(self, mainradiosystem):
        self.m = mainradiosystem
        src.logger.logInfo("Initializing IRInterface...")
        if lircinstalled:
            try:
                lirc.init(src.configs.Config.configDict["LIRC_CONFIG_PROGRAM_NAME"], src.configs.Config.configDict["LIRC_CONFIG_FILE"])
            except AttributeError:
                src.logger.logFError("Module 'lirc' has no attribute 'init'. Please install latest version from: https://pypi.python.org/pypi/python-lirc/")
                src.logger.logFError("IRInterface initialization failed.")
                mainradiosystem.shutdown()
        self.counter = 3
        self.channel = ""
        self.numkeys = ["key-zero","key-one","key-two","key-three","key-four","key-five","key-six","key-seven","key-eight","key-nine"]
        src.logger.logOk("IRInterface initialized.")

    def interpret(self, command):
        src.logger.logInfo("Received input: " + command)
        for i, j in enumerate(self.numkeys):
            if j == command:
                self.channel = self.channel+str(i)
                self.counter = self.counter - 1
                if self.counter == 0:
                    self.m.findIndexForNearestPreviousChannel(int(self.channel))
                    self.channel = ""
                    self.counter = 3
                    return
                else:
                    #Return?
                    return

        if "key-play" in command:
            self.m.play()
        elif "key-quit" in command:
            self.m.shutdown()
        elif "key-pause" in command:
            self.m.v.pause()
        elif "key-stop" in command:
            self.m.v.stop()
        elif "key-next" in command:
            self.m.nextStream()
        elif "key-prev" in command:
            self.m.previousStream()
        elif "key-nextgenre" in command:
            self.m.nextGenre()
        elif "key-previousgenre" in command:
            self.m.previousGenre()
        elif "key-volup" in command:
            self.m.v.volup(int(src.configs.Config.configDict["VOLUME_INCREMENT"]))
        elif "key-voldown" in command:
            self.m.v.voldown(int(src.configs.Config.configDict["VOLUME_INCREMENT"]))
        elif "key-previouschannel" in command:
            self.m.previousChannel()
        elif "key-mute" in command:
            self.m.v.mute_unmute()
        elif "key-move_mode_switch":
            pass
        elif "key-sounds_switch":
            pass
        elif "key-update_software":
            pass
    
    def processIRInput(self):
        if lircinstalled:
            i = lirc.nextcode()
            if len(i)>0:
                self.interpret(i[0])
        else:
            time.sleep(1)
    
    def shutdown(self):
        src.logger.logInfo("Deinitializing IRInterface...")
        if lircinstalled:
            lirc.deinit()
        src.logger.logOk("IRInterface deinitalized.")
