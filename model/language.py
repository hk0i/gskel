from lxml import etree
import os

class Language(object):
    """language object stores a language and all of its directives"""
    def __init__(self, **kwargs):
        super(Language, self).__init__()
        if 'name' in kwargs:
            self.name = kwargs['name']
        if 'alias' in kwargs:
            self.alias = kwargs['alias']

        #list of directive dicts that show {directive-names : skel-file-paths}
        self.directives = list()

    def addDirective(self, directive, skelfile):
        """adds a directive to the language"""
        directive = self.alias + '/' + directive
        self.directives.append({directive : skelfile})

    def toXml(self):
        '''returns object as xml'''
        root = etree.Element('lang')
        name = lang.SubElement('name')
        name.text = self.name

        alias = lang.SubElement('alias')
        alias.text = self.alias

class Languages(object):
    """stores a list of languages"""
    def __init__(self, langfile = None):
        super(Languages, self).__init__()
        self.langfile = langfile
        self.languages = list()

        if self.langfile:
            self.loadFile(langfile)

    def loadFile(self, filename):
        """loads a language xml file from filename"""
        if os.path.exists(filename):
            #try to load fil
            tree = etree.parse(filename)
            langs = tree.xpath('/languages/lang')
            for lang in langs:
                name  = lang.findtext('name')
                alias = lang.findtext('alias')
                self.languages.append(Language(name=name, alias=alias))

    def toXml(self):
        """returns xml of languages"""
        for lang in self.languages:
            print lang.toXml()

    def lang(self, search):
        """
        returns the Language object with name or alias `search`.
        returns None if not in self.languages
        """
        for lang in self.languages:
            if lang.name == search or lang.alias == search:
                return lang
        return None

if __name__ == '__main__':
    #test Language obj
    lang = Language(name='python', alias='py')
    print lang.name, lang.alias
    lang.addDirective('proj', '/create/project.xml')
    print lang.directives

    l = Languages('skel/language.xml')
    l.lang('C').addDirective('test','test.xml')
    l.lang('cpp').addDirective('testcpp', 'testcpp.xml')
    for lang in l.languages:
        print lang.name, lang.alias, lang.directives
