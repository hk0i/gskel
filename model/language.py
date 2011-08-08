from lxml import etree
from logger import log
from skel import Skel
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

    def getDirective(self, directive):
        """
        checks to see if `directive` exists in language.
        Returns False on failure.
        Returns skel.xml file path if language has directive
        """
        search = self.alias + '/' + directive
        if self.directives:
            log.debug('Searching for directive: ' + search)
            for d in self.directives:
                dirname = d.keys()
                dirname = dirname[0]
                if dirname == search:
                    return d[dirname]

        log.debug('Directive `' + search + '` not found in ' + self.name)
        return False

    def toXml(self):
        '''returns object as xml'''
        root = etree.Element('lang')
        name = lang.SubElement('name')
        name.text = self.name

        alias = lang.SubElement('alias')
        alias.text = self.alias

    def __str__(self):
        """to string method"""
        return self.name

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

    def loadDirectives(self, directory):
        """loads directives recursively from a directory"""
        for path, dirs, files in os.walk(directory):
            if 'skel.xml' in files:
                skelFile = os.path.join(path, 'skel.xml')
                s = Skel(skelFile)

                log.debug(
                    'Loading directive: '
                    + s.directive
                    + ' into language '
                    + s.language
                )

                lang = self.lang(s.language)
                if lang:
                    lang.addDirective(s.directive, skelFile)

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

    #test load directives
    log.notice('Attempting to load directives...')
    l.loadDirectives('skel')
    for lang in l.languages:
        print lang.name, lang.alias, lang.directives

    log.notice(
        'Checking for sample directive: proj/cli in cpp: '
        + str(l.lang('cpp').getDirective('proj/cli'))
    )

    log.notice(
        'Checking for non-existant directive: proj/main in cpp: '
        + str(l.lang('cpp').getDirective('proj/main'))
    )
