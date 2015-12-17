import subprocess, os, signal
import buttons

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
        print("Writing to file.")
        f = open('buttonsconfig.lirc','w')
        f.write(self.result)
        f.close()

    def process(line):
        button = line.split(" ")[1]
        if i<len(buttons.Buttons):
            print(buttons.Buttons[i] + " has been assigned to: " + button)
            restemplate = template.replace("{b}",button)
            restemplate = restemplate.replace("{c}",buttons.Buttons[i])
            if "key-vol" in buttons.Buttons[i]:
                restemplate = restemplate.replace("repeat = 0", "repeat = 1")
            self.result = self.result + restemplate
            i=i+1
        
        if i<len(buttons.Buttons):
            print("Please assign: "+buttons.Buttons[i])
        else:
            print("Assignment of buttons has been completed.")
            self.popen = subprocess.Popen(["kill", str(self.popen.pid)])
            complete()

    def execute(command):
        try:
            self.popen = subprocess.Popen(command, stdout=subprocess.PIPE)
            print("Please assign: "+buttons.Buttons[i])
            lines_iterator = iter(self.popen.stdout.readline, b"")
            lastline = ""
            for line in lines_iterator:
                linestring = line.decode("UTF-8")
                if lastline!=linestring:
                    process(linestring)
                lastline = linestring
                
        except KeyboardInterrupt:
            print("Assignment of buttons has been interrupted and aborted.")
            self.popen = subprocess.Popen(["kill", str(self.popen.pid)])

if __name__=="__main__":
    execute(["irw"])


