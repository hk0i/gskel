import argparse
from model.logger import Logger
from model import gskel
from model.directives import Directives
from model.language import Language

#gskel cli - commandline interface for gskel

class CLIParser(object):
    """docstring for CLIParser"""
    def __init__(self):
        super(CLIParser, self).__init__()
        self.log  = Logger()
        self.dirs = Directives()

    def parse(self):
        parser = argparse.ArgumentParser(prog='gSkel')
        #add version
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s ' + gskel.VERSION,
            help='display version information and quit'
        )

        parser.add_argument(
            '-v',
            action='store_true',
            help='verbose mode, show debug output'
        )

        parser.add_argument('lang', help='language code: c, cpp, java')
        parser.add_argument(
            'directive',
            help='instruction to perform for specified language'
        )

        args = parser.parse_args()
        if args:
            if args.v == True:
                gskel.debugModeSet = True
            self.log.debug('args: ' + str(args))
