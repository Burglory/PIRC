import subprocess, os, signal
import buttons

i = 0
popen = None
buttonmap = []

def complete():
    print("Writing to file.")
    f = open('buttonsconfig.lirc','w')
    result = ""
    for button in buttonmap:
        result = result + "," + button
    f.write(result)
    f.close()

def process(line):
    button = line.split(" ")[1]
    if i<len(buttons.Buttons):
        print(buttons.Buttons[i] + " has been assigned to: " + button)
        i=i+1
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
        for line in lines_iterator:
            process(line)
    except KeyboardInterrupt:
        print("Assignment of buttons has been interrupted.")
        popen = subprocess.Popen(["kill", str(popen.pid)])
        #popen.kill()
        #os.kill(popen.pid, signal.SIGTERM)

execute(["irw"])


