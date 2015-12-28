class Bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

LevelFError = 5
LevelError = 4
LevelOk = 3
LevelInfo = 2
LevelLog = 1

LogLevel = 3

def logFError(message):
    if LogLevel > LevelFError:
        return
    print(Bcolors.FAIL + "[ FATAL ]\t" + Bcolors.ENDC+message)

def logError(message):
    if LogLevel > LevelError:
        return
    print(Bcolors.WARNING + "[ ERROR ]\t"+ Bcolors.ENDC+message)

def logOk(message):
    if LogLevel > LevelOk:
        return
    print(Bcolors.OKGREEN + "[  OK  ]\t"+ Bcolors.ENDC+message)

def logInfo(message):
    if LogLevel > LevelInfo:
        return
    print(Bcolors.OKBLUE + "[ INFO ]\t"+ Bcolors.ENDC+message)

def log(message):
    if LogLevel > LevelLog:
        return
    print(message)
