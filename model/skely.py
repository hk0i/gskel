import os

import yaml
from logger import log
from skel import Skel

class SkelYaml(Skel):
    """skel implementation that loads yaml files"""
    def __init__(self, filename = None):
        super(SkelYaml, self).__init__()
        self.filename = filename
        if filename:
            self.loadFile(filename)

        del self.infoNodes

        #this holds a yaml skel object loaded from a file using yaml.load()
        yam = None

    def loadFile(self, filename):
        """ docstring for loadFile"""
        if os.path.exists(filename):
            log.debug('loading file: ' + filename)
            f = file(filename, 'r')
            # temporary storage for yaml information
            skel = yaml.safe_load(f)

            # info ########################################################
            self.name      = skel['name']
            self.author    = skel['author']
            self.directive = skel['directive']
            self.language  = skel['language']

            self.params  = skel['params']
            self.filelist  = skel['filelist']
        else:
            log.error(
                'could not load file: "'
                + filename + '" because it does not exist.'
            )

    def saveFile(self, filename):
        """saves skeleton to a yaml document"""
        #temporarily remove the filename attribute so that yaml.dump() won't
        #output it unnecessarily and give an incorrect filename anyway when
        #migrating between systems
        tmpfilename = self.filename
        del self.filename
        file_ = open(filename, 'w')
        file_.write(yaml.dump(self))
        file_.close()
        self.filename = tmpfilename

if __name__ == '__main__':
    skel = SkelYaml()
    skel.loadFile('skel/java/class/skel.yaml')
    skel.saveFile('test')
