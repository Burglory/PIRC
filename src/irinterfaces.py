import time
import src.logger

lircinstalled = True
try:
    import lirc
except ImportError:
    src.logger.logFError("Error: Could not import python lirc package. Is it installed?")
    lircinstalled = False

class IRInterface(object):

    def __init__(self):
        src.logger.logInfo("Initializing IRInterface...")
        if lircinstalled:
            lirc.init("lircradiosystem","lircradiosystem.lirc")
        self.counter = 3
        self.channel = ""
        self.numkeys = ["key-zero","key-one","key-two","key-three","key-four","key-five","key-six","key-seven","key-eight","key-nine"]
        src.logger.logOk("IRInterface initialized.")
        
    def readIRInput(self):
        if lircinstalled:
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
        else:
            time.sleep(1)
        return ""
    
    def shutdown(self):
        src.logger.logInfo("Deinitializing IRInterface...")
        if lircinstalled:
            lirc.deinit()
        src.logger.logOk("IRInterface deinitalized.")
