import os
import shutil
# from model import skel
from skel import Skel

class Project(object):
    """creates a project given a skeleton and a project name"""
    def __init__(self, name = None, skel = None):
        super(Project, self).__init__()

        self.project_name = name
        self.skel         = skel


    def createFiles(self, dest):
        """creates all files from the skeleton in the dest dir"""
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
                    else:
                        print '[gskel]: File exists, not creating: ' \
                                + skelFile

if __name__ == '__main__':
    s = Skel()
    s.loadFile('f.xml')

    p = Project('test_project', s)
    p.createFiles('test_output')
