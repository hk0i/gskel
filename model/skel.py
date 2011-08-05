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
        self.alias    = None
        self.language = None
        self.filelist = list()

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

            name = tree.xpath('/skel/info/name')
            self.name = name[0].text

            author = tree.xpath('/skel/info/author')
            self.author = author[0].text

            alias = tree.xpath('/skel/info/alias')
            self.alias = alias[0].text

            language = tree.xpath('/skel/info/language')
            self.language = language[0].text

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
        name = etree.SubElement(info, 'name')
        name.text = self.name
        author = etree.SubElement(info, 'author')
        author.text = self.author
        alias = etree.SubElement(info, 'alias')
        alias.text = self.alias
        language = etree.SubElement(info, 'language')
        language.text = self.language

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
    ts.alias  = 'samp'
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

