import os
import sys
from lxml import etree

import skelfactory
from logger import log
from skel import Skel
from skely import SkelYaml


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

    def add_directive(self, directive, skelfile):
        """adds a directive to the language"""
        directive = self.alias + '/' + directive
        self.directives.append({directive : skelfile})

    def get_directive(self, directive):
        """
        checks to see if `directive` exists in language.
        Returns False on failure.
        Returns skel.xml file path if language has directive
        """
        search = self.alias + '/' + directive
        if self.directives:
            log.debug('Searching for directive: ' + search)
            for d in self.directives:
                dirname = d.keys()[0]
                if dirname == search:
                    return d[dirname]

        log.error('Directive `' + search + '` not found in ' + self.name)
        sys.exit(1)
        return False

    def to_xml(self):
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
            self.load_file(langfile)

    def load_file(self, filename):
        """loads a language xml file from filename"""
        if os.path.exists(filename):
            #try to load fil
            tree = etree.parse(filename)
            langs = tree.xpath('/languages/lang')
            for lang in langs:
                name  = lang.findtext('name')
                alias = lang.findtext('alias')
                self.languages.append(Language(name=name, alias=alias))

    def load_directives(self, directory):
        """loads directives recursively from a directory"""
        log.debug('loading directives...')
        for path, dirs, files in os.walk(directory):
            for type_ in skelfactory.SKEL_TYPES:
                type_ = 'skel.' + type_
                if type_ in files:
                    log.debug('found file: ' + type_)
                    skel_file = os.path.join(path, type_)
                    s = skelfactory.create_skel(skel_file)

                    log.debug(
                        'Loading directive: '
                        + str(s.directive)
                        + ' into language '
                        + str(s.language)
                        + ' from file: '
                        + '"' + skel_file + '"'
                    )

                    lang = self.lang(s.language)
                    if lang:
                        lang.add_directive(s.directive, skel_file)

    def get_directory(self):
        """Retrieves a list of all directives by language"""
        msg = 'Lang\tDirective\tDescription\n'
        for lang in self.languages:
            msg += str(lang) + ' (' + lang.alias + ')\n'
            for dir in lang.directives:
                k = dir.keys()[0]
                skel = skelfactory.create_skel(dir[k])
                dname = '/'.join(k.split('/')[1:])
                if skel.name:
                    msg += '\t' + dname + '\t' + str(skel.name) + '\n'
                    if skel.params:
                        params = ''
                        for p in skel.params:
                            try:
                                params += p[p.keys()[0]] + ' '
                            except:
                                params += p
                        msg += '\targuments: ' + params + '\n\n'

        return msg

    def to_xml(self):
        """returns xml of languages"""
        for lang in self.languages:
            print lang.to_xml()

    def lang(self, search):
        """
        returns the Language object with name or alias `search`.
        Returns None if not in self.languages
        """
        for lang in self.languages:
            if lang.name == search or lang.alias == search:
                return lang
        return None

if __name__ == '__main__':
    #test Language obj
    lang = Language(name='python', alias='py')
    print lang.name, lang.alias
    lang.add_directive('proj', '/create/project.xml')
    print lang.directives

    l = Languages('skel/language.xml')
    l.lang('C').add_directive('test','test.xml')
    l.lang('cpp').add_directive('testcpp', 'testcpp.xml')
    for lang in l.languages:
        print lang.name, lang.alias, lang.directives

    #test load directives
    log.notice('Attempting to load directives...')
    l.load_directives('skel')
    for lang in l.languages:
        print lang.name, lang.alias, lang.directives

    log.notice(
        'Checking for sample directive: proj/cli in cpp: '
        + str(l.lang('cpp').get_directive('proj/cli'))
    )

    # log.notice(
        # 'Checking for non-existant directive: proj/main in cpp: '
        # + str(l.lang('cpp').get_directive('proj/main'))
    # )

    print l.get_directory()
