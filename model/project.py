import os
import shutil
from skel import Skel
from logger import Logger

class Project(object):
    """creates a project given a skeleton and a project name"""
    def __init__(self, name = None, skel = None):
        super(Project, self).__init__()

        self.project_name = name
        self.skel         = skel
        self.log          = Logger()

    def createFiles(self, dest):
        """copies all files from the skeleton in the dest dir"""
        if self.skel:
            for skelFile in self.skel.filelist:
                if os.path.exists(skelFile):
                    destFile = os.path.join(dest, skelFile)
                    destPath = os.path.abspath(destFile)
                    destPath = os.path.dirname(destPath)
                    if not os.path.exists(destPath):
                        os.makedirs(destPath)
                    if not os.path.exists(destFile):
                        shutil.copyfile(skelFile, destFile)
                        self.log.notice(
                            'Creating file: '
                            + destFile
                        )
                    else:
                        self.log.warning(
                            'File exists, skipping: '
                            + skelFile
                        )

if __name__ == '__main__':
    s = Skel()
    s.loadFile('f.xml')

    p = Project('test_project', s)
    p.createFiles('test_output')
