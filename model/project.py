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
            {'AUTHOR'     : gskel.config.authorName},
            {'AUTHOREMAIL': gskel.config.authorEmail}
        ]

    def repWord(self, string, word, rep):
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

    def repVars(self, skel, string):
        """replaces variables in file filename according to skel object"""

        fContent = string
        if skel.hasParams() and self.params:
            log.debug(
                'Attempting to make variable replacements.'
            )
            i = 0
            for param in skel.params:
                pVal = param.keys()[0]
                pVal = param[pVal]
                log.debug('param data: ' + pVal)
                fContent = self.repWord(fContent, pVal, self.params[i])
                i = i + 1

        log.debug('Replacing constants..')
        for const in self.constants:
            key = const.keys()[0]
            rep= const[key]
            fContent = self.repWord(fContent, key, rep)

        return fContent

    def repVarsFile(self, skel, filename):
        """replaces variables in file filename according to skel object"""
        log.debug(
            'Attempting to make variable replacements in file: '
            + filename
        )
        f = open(filename, 'r')
        fContent = f.read()
        fname = filename
        f.close()

        #replace content
        fContent = self.repVars(skel, fContent)
        fname = self.repVars(skel, filename)

        f = open(filename, 'w')
        f.write(fContent)
        f.close()
        return fname

    def createFiles(self, dest):
        """copies all files from the skeleton in the dest dir"""
        log.debug('Project::createFiles: creating files.')
        if self.skel:
            for skelFile in self.skel.filelist:
                #full path to source file
                sourceFile = os.path.join(
                    os.path.dirname(self.skel.filename), skelFile
                )
                log.debug(
                    'Project::createFiles: checking for file: '
                    + sourceFile
                )
                if len(self.params) != len(self.skel.params):
                    log.error('Incorrect number of arguments; aborting...')
                    sys.exit(1)
                if os.path.exists(sourceFile):
                    destFile = os.path.join(dest, skelFile)
                    destPath = os.path.abspath(destFile)
                    destPath = os.path.dirname(destPath)
                    if not os.path.exists(destPath):
                        log.notice(
                            'directory does not exist, '
                           + 'creating: ' + destPath
                        )
                        os.makedirs(destPath)
                    if not os.path.exists(destFile):
                        shutil.copyfile(sourceFile, destFile)
                        renamed = self.repVarsFile(
                            self.skel,
                            destFile
                        )
                        nFile = destFile
                        if renamed != destFile:
                            shutil.move(destFile, renamed)
                            nFile = renamed
                        log.notice(
                            'Created file: '
                            + nFile
                        )
                    else:
                        log.warning(
                            'File exists, skipping: '
                            + skelFile
                        )
                else:
                    log.error(
                        'Project::createFiles: could not copy file from '
                        + 'skeleton because it does not exist: '
                        + sourceFile
                    )
                    sys.exit(1)
        else:
            log.debug('Project::createFiles: no skel file set, aborting...')

if __name__ == '__main__':
    s = Skel()
    s.loadFile('f.xml')

    p = Project('test_project', s)
    p.createFiles('test_output')
