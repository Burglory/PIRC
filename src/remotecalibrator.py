import subprocess, os, signal
import buttons

i = 0
popen = None
result = ""
template = """\
begin
    prog = lircradiosystem
    button = {b}
    config = {c}
    repeat = 0
end
"""

def complete():
    print("Writing to file.")
    f = open('buttonsconfig.lirc','w')
    f.write(result)
    f.close()

def process(line):
    button = line.split(" ")[1]
    if i<len(buttons.Buttons):
        print(buttons.Buttons[i] + " has been assigned to: " + button)
        restemplate = template.repace("{b}",button)
        restemplate = restemplate.replace("{c}",buttons.Buttons[i])
        if "key-vol" in buttons.Buttons[i]:
            restemplate = restemplate.replace("repeat = 0", "repeat = 1")
        result = result + restemplate
        i=i+1
        
    if i<len(buttons.Buttons):
        print("Please assign: "+buttons.Buttons[i])
    else:
        print("Assignment of buttons has been completed.")
        popen = subprocess.Popen(["kill", str(popen.pid)])
        complete()

def execute(command):
    try:
        popen = subprocess.Popen(command, stdout=subprocess.PIPE)
        print("Please assign: "+buttons.Buttons[i])
        lines_iterator = iter(popen.stdout.readline, b"")
        lastline = ""
        for line in lines_iterator:
            linestring = line.decode("UTF-8")
            if lastline!=linestring:
                process(linestring)
            lastline = linestring
            
    except KeyboardInterrupt:
        print("Assignment of buttons has been interrupted.")
        popen = subprocess.Popen(["kill", str(popen.pid)])
        #popen.kill()
        #os.kill(popen.pid, signal.SIGTERM)

execute(["irw"])


