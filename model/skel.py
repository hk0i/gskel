from lxml import etree
from logger import log
import os

class Skel(object):
    """Class to represent a gskel skeleton file"""
    def __init__(self, filename = None):
        super(Skel, self).__init__()
        self.filename = filename

        self.filelist = list()

        #these nodes all become attributes of the Skel class
        #this list defines the attribute : xpath to node text data
        self.info_nodes = [
            {'name'      : '/skel/info/name' },
            {'author'    : '/skel/info/author'},
            {'language'  : '/skel/info/language'},
            {'directive' : '/skel/info/directive'}
        ]

        #list of optional parameters
        self.params = list()

        #initialize the attributes to None
        for node in self.info_nodes:
            keys = node.keys()
            attr_name = keys[0]
            self.__dict__[attr_name] = None

        if filename:
            self.load_file(filename)

    def add_file(self, filename):
        """adds a file to the filelist"""
        self.filelist.append(filename)

    def remove_file(self, filename):
        """removes a file from the filelist"""
        self.filelist.remove(filename)

    def has_params(self):
        """returns True if this skeleton has extra parameters or not"""
        if self.params:
            return True
        return False

    def load_file(self, filename):
        """loads skeleton information from file"""
        if os.path.exists(filename):
            log.debug('loading file: ' + filename)
            self.filename = filename
            #try to load the file
            try:
                tree = etree.parse(filename)
                skel = tree.getroot()

                for node in self.info_nodes:
                    keys = node.keys()
                    attr_name = keys[0]
                    attr_path = node[attr_name]
                    node_data = tree.xpath(attr_path)
                    if node_data:
                        self.__dict__[attr_name] = node_data[0].text

                #get file list
                filelist = tree.xpath('/skel/filelist/file')
                for fil in filelist:
                    self.filelist.append(fil.get('name'))

                #parameters
                params = tree.xpath('/skel/params/param')
                for param in params:
                    self.params.append({param.get('name'): param.get('value')})

            except Exception as ex:
                log.warning(
                    'Could not parse skeleton file: '
                    + str(ex)
                    + ' in file: '
                    + filename
                )
                return False

        else:
            log.error('File does not exist: ' + filename)
            return False

    def to_xml(self):
        """returns xml representation of the object"""
        #root skel node ###################################################
        skel = etree.Element('skel')

        #info node ########################################################
        info = etree.SubElement(skel, 'info')
        skel.append(info)

        #info data ########################################################
        for node in self.info_nodes:
            keys = node.keys()
            attr_name = keys[0]
            xml_node = etree.SubElement(info, attr_name)
            xml_node.text = self.__dict__[attr_name]

        #parameters #######################################################
        params = etree.SubElement(skel, 'params')

        for param in self.params:
            param_name = param.keys()[0]
            xml_node = etree.SubElement(params, 'param')
            xml_node.set('name', param_name)
            xml_node.set('value', param[param_name])

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

    def get_xml(self):
        """wrapper function for to_xml, returns object as xml"""
        return self.to_xml()

    def save_file(self, filename):
        """Save file"""

        xml = self.get_xml()

        #write to file
        f = open(filename, 'w')
        f.write(xml)
        f.close()

if __name__ == "__main__":
    log.notice('Running test cases for Skel...')

    log.notice('Creating test object...')
    ts = Skel()
    log.notice('Attempting to open a file that does not exist...')
    ts.load_file('this-does-not-exist.xml')
    ts.name = 'sample file'
    ts.author = 'sample author'
    ts.directive  = 'samp'
    ts.language = 'C++'
    ts.add_file('main.cpp')
    ts.add_file('this should not appear')
    ts.remove_file('this should not appear')
    log.notice('Writing test object to file f.xml...')
    ts.save_file('f.xml')

    log.notice('Loading test file...')
    tl = Skel()
    tl.load_file('skel/cpp/cli/skel.xml')
    print tl.get_xml()

    log.notice('Loading f.xml')
    tl2 = Skel()
    tl2.load_file('f.xml')
    print tl2.get_xml()

    log.notice('loading test skel with replacement vars...')
    tl3 = Skel('skel/java/main-class/skel.xml')
    print tl3.get_xml()

