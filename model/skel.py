from lxml import etree
import os

class Skel(object):
    """Class to represent a gskel skeleton file"""
    def __init__(self, filename = None):
        super(Skel, self).__init__()
        self.filename = filename

        self.name     = None
        self.author   = None
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
    ts = Skel()
    ts.name = 'sample file'
    ts.author = 'sample author'
    ts.addFile('main.cpp')
    ts.addFile('this should not appear')
    ts.removeFile('this should not appear')
    ts.saveFile('f.xml')

    tl = Skel()
    tl.loadFile('skel/cpp/cli/skel.xml')
    print tl.getXml()

