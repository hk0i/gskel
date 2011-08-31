import argparse
import os
import sys

from model.logger import log
from model import gskel
from model.language import Language, Languages
from model.project import Project
from model import skelfactory

#gskel cli - commandline interface for gskel

class CLIParser(object):
    """docstring for CLIParser"""
    def __init__(self):
        super(CLIParser, self).__init__()

    def parse(self):
        parser = argparse.ArgumentParser(prog='gskel')
        #add version
        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s ' + gskel.VERSION,
            help='display version information and quit'
        )

        parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='verbose mode, show debug output'
        )

        parser.add_argument(
            '-l',
            '--list',
            action='store_true',
            help='list available directives and exit'
        )

        parser.add_argument(
            '-p',
            '--project-name',
            help='Name of the project',
            default='Unnamed'
        )

        parser.add_argument('lang', help='language id: c, cpp, java')
        parser.add_argument(
            'directive',
            help='instruction to perform for specified language'
        )

        parser.add_argument(
            'params',
            help='arguments for directive',
            nargs='*',
            default=None
        )

        parser.add_argument(
            '-o',
            '--outpath',
            help='directory to output to, defaults to current directory',
            default='.'
        )

        args = parser.parse_args()

        ###################################################################
        # For the love of god, please make sure debug mode is checked BEFORE
        # ANYTHING ELSE -- Otherwise certain methods won't get debug output
        ###################################################################
        if args:
            if args.verbose == True:
                gskel.config.debugModeSet = True
            log.debug('args: ' + str(args))
        ###################################################################
        # i.e., insert new code BELOW THIS LINE
        # ... unless it requires adding new command line args.
        ###################################################################


        #find languages and add args for each
        #add an arg for each lang name, then pass the directive as an arg to it
        langs = Languages(os.path.join(sys.path[0], 'skel/language.xml'))
        langs.loadDirectives(os.path.join(sys.path[0], 'skel'))
        if args.list:
            print langs.getDirectory()
            sys.exit(0)
        skelFile = None

        if args.directive and args.outpath:
            for lang in langs.languages:
                log.debug('acquiring skel file for: ' + args.directive)
                lang = langs.lang(args.lang)
                if lang:
                    skelFile = lang.getDirective(args.directive)
                    log.debug('skel file found: ' + str(skelFile))
                    break
                else:
                    log.error(
                        'No language definition found for lang `'
                        + args.lang
                        + '`'
                    )
                    sys.exit(1)

            #copy files
            if skelFile:
                skeleton = skelfactory.create_skel(skelFile)
                project = Project(
                    name = args.project_name,
                    skel = skeleton,
                    params = args.params
                )
                project.createFiles(args.outpath)

