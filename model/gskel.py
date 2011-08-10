try:
    import os
except:
    pass

import ConfigParser

VERSION = '1.0'
HOME_PATH = os.getenv('USERPROFILE') or os.getenv('HOME')

class Config(object):
    """docstring for Config"""
    def __init__(self):
        super(Config, self).__init__()

        self.debugModeSet = False
        self.authorName  = 'gskel'
        self.authorEmail = 'nobody@localhost'

        self.config = ConfigParser.SafeConfigParser()
        configPath = os.path.join(HOME_PATH, '.gskel', 'config')
        if os.path.exists(configPath):
            self.loadConfig(configPath)

    def loadConfig(self, configPath):
        """loads configuration into model from an existing config file"""
        self.config.readfp(open(configPath, 'r'))
        if self.config.has_section('debug'):
            self.debugModeSet = self.config.getboolean('debug', 'enabled')

        #default author info
        if self.config.has_section('author'):
            self.authorName   = self.config.get('author', 'name', 'gskel')
            self.authorEmail  = self.config.get(
                'author',
                'email',
                'nobody@localhost'
            )


config = Config()
