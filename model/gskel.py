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

        self.debug_mode_set = False
        self.author_name  = 'gskel'
        self.author_email = 'nobody@localhost'

        self.config = ConfigParser.SafeConfigParser()
        config_path = os.path.join(HOME_PATH, '.gskel', 'config')
        if os.path.exists(config_path):
            self.load_config(config_path)

    def load_config(self, config_path):
        """loads configuration into model from an existing config file"""
        self.config.readfp(open(config_path, 'r'))
        if self.config.has_section('debug'):
            self.debug_mode_set = self.config.getboolean('debug', 'enabled')

        #default author info
        if self.config.has_section('author'):
            self.author_name   = self.config.get('author', 'name', 'gskel')
            self.author_email  = self.config.get(
                'author',
                'email',
                'nobody@localhost'
            )


config = Config()
