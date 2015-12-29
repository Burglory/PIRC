import argparse
import os
import src.logger
import src.configs

parser = argparse.ArgumentParser(description='Control VLC player via an infrared remote control.')
parser.add_argument('-u', '--update', action='store_true', required=False, help='Update the current version to a newer version.', dest='update')
parser.add_argument('-v', action='store_true',required = False, help='Set more verbose output.',dest='verbose')
parser.add_argument('-vv', action='store_true',required = False, help='Set even more verbose output.',dest='fullverbose')
parser.add_argument('-q','--quiet', action='store_true',required = False, help='Show no output.',dest='quiet')
parser.add_argument('-c','--config', action='store',type=argparse.FileType('r'),required = False, help='Specify config file. Default is %s' % src.configs.Config.defaultconfigfilename,dest='config',
                    #default=src.configs.Config.defaultconfigfilename
                    )
parser.add_argument('-g','--generate', action='store_true',required = False, help='Generate template config file.', dest='generate')


def parse(mainradiosystem, args):
    args = parser.parse_args(args)
    if args.verbose:
        src.logger.LogLevel = 2
    if args.fullverbose:
        src.logger.LogLevel = 1
    if args.quiet:
        src.logger.LogLevel = 99
    if args.generate:
        src.configs.Config.save(src.configs.Config.configDict)
    if args.config:
        src.configs.Config(args.config.name)
    else:
        src.configs.Config()
    if args.update:
        print("Update time!")
