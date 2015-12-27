import argparse

parser = argparse.ArgumentParser(prog='PIRC', description='Control VLC player via an infrared remote control.')
parser.add_argument('-U', '--update', action='store_true', required=False, help='Update the current version to a newer version.', dest='update')

def parse(mainradiosystem, args):
    args = parser.parse_args(args)
    if args.update:
        print("Update time!")
        
