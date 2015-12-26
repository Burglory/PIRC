class Bcolors(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def logFError(message):
    print(Bcolors.FAIL + "[ FATAL ]\t"+message + Bcolors.ENDC)

def logError(message):
    print(Bcolors.WARNING + "[ ERROR ]\t"+message + Bcolors.ENDC)

def logOk(message):
    print(Bcolors.OKGREEN + "[  OK  ]\t"+message + Bcolors.ENDC)

def logInfo(message):
    print(Bcolors.OKBLUE + "[ INFO ]\t"+message + Bcolors.ENDC)

def log(message):
    print(message)
