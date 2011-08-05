from lxml import etree
from logger import Logger
import os

class Skel(object):
    """Class to represent a gskel skeleton file"""
    def __init__(self, filename = None):
        super(Skel, self).__init__()
        self.filename = filename

        self.name     = None
        self.author   = None
        self.directive    = None
        self.language = None
        self.filelist = list()

        #these nodes all become attributes of the Skel class
        #this list defines the attribute : xpath to node text data
        self.infoNodes = [
            {'name'      : '/skel/info/name' },
            {'author'    : '/skel/info/author'},
            {'language'  : '/skel/info/language'},
            {'directive' : '/skel/info/directive'}
        ]

    def addFile(self, filename):
        """adds a file to the filelist"""
        self.filelist.append(filename)

    def removeFile(self, filename):
        """removes a file from the filelist"""
        self.filelist.remove(filename)

    def loadFile(self, filename):
        """loads skeleton information from file"""
        if os.path.exists(filename):
            #try to load the file
            tree = etree.parse(filename)
            skel = tree.getroot()

            for node in self.infoNodes:
                keys = node.keys()
                attrName = keys[0]
                attrPath = node[attrName]
                nodeData = tree.xpath(attrPath)
                self.__dict__[attrName] = nodeData[0].text

            #get file list
            filelist = tree.xpath('/skel/filelist/file')
            for fil in filelist:
                self.filelist.append(fil.get('name'))

        else:
            print 'File does not exist: ' + filename

    def getXml(self):
        """returns xml representation of the object"""
        #root skel node ###################################################
        skel = etree.Element('skel')

        #info node ########################################################
        info = etree.SubElement(skel, 'info')
        skel.append(info)

        #info data ########################################################
        for node in self.infoNodes:
            keys = node.keys()
            attrName = keys[0]
            xmlNode = etree.SubElement(info, attrName)
            xmlNode.text = self.__dict__[attrName]

        #filelist #########################################################
        filelist = etree.SubElement(skel, 'filelist')

        for fil in self.filelist:
            fnode = etree.SubElement(filelist, 'file')
            fnode.set('name', fil)

        #generate xml
        xml = etree.tostring(
            skel,
            xml_declaration = True,
            pretty_print = True,
            encoding = 'utf-8'
        )

        return xml

    def saveFile(self, filename):
        """Save file"""

        xml = self.getXml()

        #write to file
        f = open(filename, 'w')
        f.write(xml)
        f.close()

if __name__ == "__main__":
    log = Logger()
    log.notice('Running test cases for Skel...')

    log.notice('Creating test object...')
    ts = Skel()
    ts.name = 'sample file'
    ts.author = 'sample author'
    ts.directive  = 'samp'
    ts.language = 'C++'
    ts.addFile('main.cpp')
    ts.addFile('this should not appear')
    ts.removeFile('this should not appear')
    log.notice('Writing test object to file f.xml...')
    ts.saveFile('f.xml')

    log.notice('Loading test file...')
    tl = Skel()
    tl.loadFile('skel/cpp/cli/skel.xml')
    print tl.getXml()

    log.notice('Loading f.xml')
    tl2 = Skel()
    tl2.loadFile('f.xml')
    print tl2.getXml()

