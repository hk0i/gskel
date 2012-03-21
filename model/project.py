import os
import shutil
import gskel
import sys

from skel import Skel
from logger import log

class Project(object):
    """creates a project given a skeleton and a project name"""
    def __init__(self, name = None, skel = None, params = None):
        super(Project, self).__init__()

        self.project_name = name
        self.skel         = skel
        #argument *VALUES* given from cli as a list
        self.params       = params
        if self.skel.params and not self.params:
            log.error(
                'Directive `'
                + self.skel.directive
                + '` requires arguments; exiting...'
            )
            sys.exit(1)

        #some default values
        self.constants = [
            {'APPNAME'    : self.project_name},
            {'AUTHOR'     : gskel.config.author_name},
            {'AUTHOREMAIL': gskel.config.author_email}
        ]

    def rep_word(self, string, word, rep):
        replacement = str(rep)
        search = '%' + word + '%'
        log.debug(
            'Replacing %s with %s'
            % (word, replacement)
        )
        ret = string.replace(
            search,
            replacement
        )
        search = '$' + word + '$'
        ret = ret.replace(
            search,
            replacement.upper()
        )
        return ret

    def rep_vars(self, skel, string):
        """replaces variables in a string according to skel object"""

        f_content = string
        if skel.has_params() and self.params:
            log.debug(
                'Attempting to make variable replacements.'
            )
            i = 0
            for param in skel.params:
                #duck type trial and error:
                try:
                    #try to use the Skel class's XML key-value pairs
                    p_val = param.keys()[0]
                    p_val = param[p_val]
                except:
                    #every other type of Skeleton (non-XML)
                    p_val = param

                log.debug('param data: ' + p_val)
                f_content = self.rep_word(f_content, p_val, self.params[i])
                i = i + 1

        log.debug('Replacing constants..')
        for const in self.constants:
            key = const.keys()[0]
            rep= const[key]
            f_content = self.rep_word(f_content, key, rep)

        return f_content

    def rep_vars_file(self, skel, filename):
        """replaces variables in file filename according to skel object"""
        log.debug(
            'Attempting to make variable replacements in file: '
            + filename
        )
        f = open(filename, 'r')
        f_content = f.read()
        fname = filename
        f.close()

        #replace content
        f_content = self.rep_vars(skel, f_content)
        fname = self.rep_vars(skel, filename)

        f = open(filename, 'w')
        f.write(f_content)
        f.close()
        return fname

    def create_files(self, dest):
        """copies all files from the skeleton in the dest dir"""
        log.debug('creating files.')
        if self.skel:
            for skel_file in self.skel.filelist:
                #full path to source file
                source_file = os.path.join(
                    os.path.dirname(self.skel.filename),
                    os.path.basename(skel_file)
                )
                log.debug(
                    'checking for file: '
                    + source_file
                )
                if len(self.params) != len(self.skel.params):
                    log.error('Incorrect number of arguments; aborting...')
                    paramlist = list()
                    for p in self.skel.params:
                        paramlist.append(p.keys()[0])
                    log.error('expected: ' + ' '.join(paramlist))

                    sys.exit(1)
                if os.path.exists(source_file):
                    dest_file = os.path.join(
                        dest,
                        self.rep_vars(self.skel, skel_file)
                    )
                    dest_path = os.path.abspath(dest_file)
                    dest_path = os.path.dirname(dest_path)
                    if not os.path.exists(dest_path):
                        log.notice(
                            'directory does not exist, '
                           + 'creating: ' + dest_path
                        )
                        os.makedirs(dest_path)
                    if not os.path.exists(dest_file):
                        shutil.copyfile(source_file, dest_file)
                        renamed = self.rep_vars_file(
                            self.skel,
                            dest_file
                        )
                        n_file = dest_file
                        if renamed != dest_file:
                            shutil.move(dest_file, renamed)
                            n_file = renamed
                        log.notice(
                            'Created file: '
                            + n_file
                        )
                    else:
                        log.warning(
                            'File exists, skipping: '
                            + skel_file
                        )
                else:
                    log.error(
                        'could not copy file from '
                        + 'skeleton because it does not exist: '
                        + source_file
                    )
                    sys.exit(1)
        else:
            log.debug('no skel file set, aborting...')

if __name__ == '__main__':
    s = Skel()
    s.load_file('f.xml')

    p = Project('test_project', s)
    p.create_files('test_output')
