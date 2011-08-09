import argparse
import os
import sys

from model.logger import log
from model import gskel
from model.directives import Directives
from model.language import Language, Languages
from model.project import Project
from model.skel import Skel

#gskel cli - commandline interface for gskel

class CLIParser(object):
    """docstring for CLIParser"""
    def __init__(self):
        super(CLIParser, self).__init__()
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

        parser.add_argument(
            'params',
            help='arguments for directive',
            nargs='+'
        )

        parser.add_argument(
            '-o',
            '--outpath',
            help='directory to output to',
        )

        args = parser.parse_args()

        #find languages and add args for each
        #add an arg for each lang name, then pass the directive as an arg to it
        langs = Languages(os.path.join(sys.path[0], 'skel/language.xml'))
        langs.loadDirectives(os.path.join(sys.path[0], 'skel'))
        skelFile = None
        if args.directive and args.outpath:
            for lang in langs.languages:
                log.debug('acquiring skel file for: ' + args.directive)
                skelFile = langs.lang(args.lang).getDirective(args.directive)
                log.debug('skel file found: ' + str(skelFile))
                break

            #copy files
            if skelFile:
                skeleton = Skel(skelFile)
                project = Project(skel = skeleton, params = args.params)
                project.createFiles(args.outpath)

        if args:
            if args.v == True:
                gskel.debugModeSet = True
            log.debug('args: ' + str(args))
