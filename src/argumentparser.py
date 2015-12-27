import argparse
import src.logger

parser = argparse.ArgumentParser(prog='PIRC', description='Control VLC player via an infrared remote control.')
parser.add_argument('-U', '--update', action='store_true', required=False, help='Update the current version to a newer version.', dest='update')
parser.add_argument('-v', action='store_true',required = False, help='Set more verbose output.',dest='verbose')
parser.add_argument('-vv', action='store_true',required = False, help='Set even more verbose output.',dest='fullverbose')
parser.add_argument('-q','--quiet', action='store_true',required = False, help='Show no output.',dest='quiet')

def parse(mainradiosystem, args):
    args = parser.parse_args(args)
    print(args)
    if args.update:
        print("Update time!")
    if args.verbose:
        src.logger.LogLevel = 2
    if args.fullverbose:
        src.logger.LogLevel = 1
    if args.quiet:
        src.logger.LogLevel = 99
        
