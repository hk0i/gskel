import os
import shutil
from skel import Skel
from logger import log

class Project(object):
    """creates a project given a skeleton and a project name"""
    def __init__(self, name = None, skel = None, params = None):
        super(Project, self).__init__()

        self.project_name = name
        self.skel         = skel
        #argument values given from cli
        self.params       = params

    def repVars(self, skel, filename):
        """replaces variables in file filename according to skel object"""
        if skel.hasParams():
            log.debug(
                'Attempting to make variable replacements in file: '
                + filename
            )
            f = open(filename, 'r')
            fContent = f.read()
            fname = filename
            f.close()
            i = 0
            for param in skel.params:
                pVal = param.keys()[0]
                pVal = param[pVal]
                fContent = fContent.replace(pVal, self.params[i])
                fname = fname.replace(pVal, self.params[i])
                i = i + 1
            f = open(filename, 'w')
            f.write(fContent)
            f.close()
            return fname
        return False

    def createFiles(self, dest):
        """copies all files from the skeleton in the dest dir"""
        #TODO: file renaming and replacing for classes, etc...
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
                        log.notice(
                            'Creating file: '
                            + destFile
                        )
                        shutil.copyfile(sourceFile, destFile)
                        renamed = self.repVars(
                            self.skel,
                            destFile
                        )
                        if renamed:
                            shutil.move(destFile, renamed)
                    else:
                        log.warning(
                            'File exists, skipping: '
                            + skelFile
                        )
                else:
                    log.debug(
                        'Project::createFiles: could not copy file from '
                        + 'skeleton because it does not exist: '
                        + sourceFile
                    )
        else:
            log.debug('Project::createFiles: no skel file set, aborting...')

if __name__ == '__main__':
    s = Skel()
    s.loadFile('f.xml')

    p = Project('test_project', s)
    p.createFiles('test_output')
