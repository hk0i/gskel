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

    def show_directory_and_quit(self):
        '''
        hackish way of showing directory for --list and -l
        '''
        #this is the only way I came up with to get around the min arg number
        langs = Languages(os.path.join(sys.path[0], 'skel/language.xml'))
        langs.load_directives(os.path.join(sys.path[0], 'skel'))
        print langs.get_directory()
        sys.exit(0)

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

        #until I figure out a way to make this option ignore the other required
        #options this is actually only handled by the show_directory_and_quit
        #function above. It is included in here soley for the output of
        #gskel -h
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

        if len(sys.argv) == 2 and (sys.argv[1] == '-l' or sys.argv[1] == '--list'):
            self.show_directory_and_quit()

        args = parser.parse_args()

        ###################################################################
        # For the love of god, please make sure debug mode is checked BEFORE
        # ANYTHING ELSE -- Otherwise certain methods won't get debug output
        ###################################################################
        if args:
            if args.verbose == True:
                gskel.config.debug_mode_set = True
            log.debug('args: ' + str(args))
        ###################################################################
        # i.e., insert new code BELOW THIS LINE
        # ... unless it requires adding new command line args.
        ###################################################################


        #find languages and add args for each
        #add an arg for each lang name, then pass the directive as an arg to it
        langs = Languages(os.path.join(sys.path[0], 'skel/language.xml'))
        langs.load_directives(os.path.join(sys.path[0], 'skel'))
        if args.list:
            print langs.get_directory()
            sys.exit(0)
        skel_file = None

        if args.directive and args.outpath:
            for lang in langs.languages:
                log.debug('acquiring skel file for: ' + args.directive,
                        self)
                lang = langs.lang(args.lang)
                if lang:
                    skel_file = lang.get_directive(args.directive)
                    log.debug('skel file found: ' + str(skel_file))
                    break
                else:
                    log.error(
                        'No language definition found for lang `'
                        + args.lang
                        + '`'
                    )
                    sys.exit(1)

            #copy files
            if skel_file:
                skeleton = skelfactory.create_skel(skel_file)
                project = Project(
                    name = args.project_name,
                    skel = skeleton,
                    params = args.params
                )
                project.create_files(args.outpath)

