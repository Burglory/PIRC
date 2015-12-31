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

def logFError(message, force=False):
    if LogLevel > LevelFError and not force:
        return
    _print(Bcolors.FAIL + "[ FATAL ]\t" + Bcolors.ENDC+message)

def logError(message, force=False):
    if LogLevel > LevelError and not force:
        return
    _print(Bcolors.WARNING + "[ ERROR ]\t"+ Bcolors.ENDC+message)

def logOk(message, force=False):
    if LogLevel > LevelOk and not force:
        return
    _print(Bcolors.OKGREEN + "[  OK  ]\t"+ Bcolors.ENDC+message)

def logInfo(message, force=False):
    if LogLevel > LevelInfo and not force:
        return
    _print(Bcolors.OKBLUE + "[ INFO ]\t"+ Bcolors.ENDC+message)

def log(message, force=False):
    if LogLevel > LevelLog and not force:
        return
    _print(message)

def _print(message):
    print(message)