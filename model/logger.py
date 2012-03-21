import sys
import os
import datetime
import inspect

import gskel

class Logger(object):
    """logs to stdout and/or log files"""
    def __init__(self, logfile = None):
        super(Logger, self).__init__()

        #constants
        self.GRAY      = 30
        self.GREY      = 30
        self.RED       = 31
        self.GREEN     = 32
        self.YELLOW    = 33
        self.BLUE      = 34
        self.MAGENTA   = 35
        self.CYAN      = 36
        self.WHITE     = 37
        self.RESET     = '\033[1;m'

        #attributes
        self.logfile = logfile
        self.use_time = False

    def color(self, color, bold = False):
        """returns a color based on the input"""
        if bold:
            bold = 1
        else:
            bold = 0
        return '\033[' + str(bold) + ';' + str(color) + 'm'

    def set_time(self, value = True):
        """enables or disables timestamps"""
        self.use_time = value

    def current_time(self):
        """
        returns the current time in a standard format and a trailing space
        """
        now = datetime.datetime.now()
        if self.use_time == True:
            return now.strftime('%Y.%m.%d %H:%M:%S ')
        else:
            return ''

    def cprint(self, msg, color, bold = False):
        """prints a message in color"""
        msgs = msg.split('[')
        m_type = msgs[1]
        msgs = m_type.split(']')
        m_type = msgs[0]
        if sys.stdout.isatty():
            print(self.current_time()
                + '[' + self.color(color, bold) +  m_type + self.RESET + ']'
                + msgs[1]
            )
        else:
            print msg

    def debug(self, msg, classref = None):
        """prints a debug message only when debug mode is on"""
        if gskel.config.debug_mode_set:
            stack = inspect.stack()[1]
            caller = stack[3]
            if caller != '?':
                if not classref:
                    module = os.path.basename(stack[1])
                else:
                    module = classref.__class__.__name__
                debuginfo = '(' + module + ') ' \
                    + caller + '(): '
            msg = '[debug] ' + debuginfo + msg
            self.cprint(msg, self.GREEN, True)

    def notice(self, msg):
        """docstring for notice"""
        msg = '[notice] ' + msg
        self.cprint(msg, self.BLUE, True)

    def warning(self, msg):
        """prints a warning"""
        msg = '[warning] ' + msg
        self.cprint(msg, self.YELLOW, True)

    def error(self, msg):
        msg = '[error] ' + msg
        """prints an error message"""
        self.cprint(msg, self.RED, True)

log = Logger()

if __name__ == '__main__':
    l = Logger()
    l.notice('notice')
    l.set_time()
    l.warning('warning')
    l.error('error')
