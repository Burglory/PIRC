import subprocess, os, signal
import src.buttons
import src.logger
import src.configs

class RemoteCalibrator(object):

    def __init__(self):
        self.i = 0
        self.popen = None
        self.result = ""
        self.template = """\
begin
    prog = lircradiosystem
    button = {b}
    config = {c}
    repeat = 0
end
"""

    def complete(self):
        src.logger.logInfo("Writing to file.", force=True)
        f = open(src.configs.Config.configDict["LIRC_CONFIG_FILE"],'w')
        f.write(self.result)
        f.close()
        src.logger.logOk("Config written to file.", force=True)

    def process(self, line):
        button = line.split(" ")[1]
        if i<len(buttons.Buttons):
            src.logger.logOk(buttons.Buttons[i] + " has been assigned to: " + button, force=True)
            restemplate = template.replace("{b}",button)
            restemplate = restemplate.replace("{c}",buttons.Buttons[i])
            if "key-vol" in buttons.Buttons[i]:
                restemplate = restemplate.replace("repeat = 0", "repeat = 1")
            self.result = self.result + restemplate
            i=i+1
        
        if i<len(buttons.Buttons):
            src.logger.logInfo("Please assign: "+buttons.Buttons[i], force=True)
        else:
            src.logger.logOk("Assignment of buttons has been completed.", force=True)
            self.popen = subprocess.Popen(["kill", str(self.popen.pid)])
            self.complete()

    def execute(self, command):
        try:
            self.popen = subprocess.Popen(command, stdout=subprocess.PIPE)
            src.logger.logInfo("Please assign: "+buttons.Buttons[i], force=True)
            lines_iterator = iter(self.popen.stdout.readline, b"")
            lastline = ""
            for line in lines_iterator:
                linestring = line.decode("UTF-8")
                if lastline!=linestring:
                    self.process(linestring)
                lastline = linestring
                
        except KeyboardInterrupt:
            src.logger.logFError("Assignment of buttons has been interrupted and aborted.", force=True)
            self.popen = subprocess.Popen(["kill", str(self.popen.pid)])

    def runCalibrator(self):
        self.execute(["irw"])
        
if __name__=="__main__":
    execute(["irw"])


