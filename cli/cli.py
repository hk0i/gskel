import argparse
from model.logger import Logger
from model import gskel

#gskel cli - commandline interface for gskel

class CLIParser(object):
    """docstring for CLIParser"""
    def __init__(self):
        super(CLIParser, self).__init__()

    def parse(self):
        parser = argparse.ArgumentParser(prog='gSkel')
        #add version
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version='%(prog)s ' + gskel.VERSION,
            help='display version information and quit'
        )

        parser.add_argument('lang', help='language code: c, cpp, java')
        parser.add_argument(
            'directive',
            help='instruction to perform for specified language'
        )

        args = parser.parse_args()
        if args:
            print args
