import sys

from gsprinter import GSPrinter

Printer = 'cli'

NoIcon = ''
NoticeIcon = 'notice'
WarningIcon = 'warning'
ErrorIcon = 'error'

class CliPrinter(GSPrinter):
    """command line implementation for message output"""

    def __init__(self):
        """set up some attributes"""

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
        self.RESET     = '\033[0;m'

        #need to find a better way to do this...
        self.NoIcon = NoIcon
        self.NoticeIcon = NoticeIcon
        self.WarningIcon = WarningIcon
        self.ErrorIcon = ErrorIcon

    def color(self, color, bold = False):
        """returns a color based on the input"""
        if bold:
            bold = 1
        else:
            bold = 0
        return '\033[' + str(bold) + ';' + str(color) + 'm'

    def colorize_icon(self, icon):
        """colorizes icon when console supports it"""
        if icon != NoIcon:
            if sys.stdout.isatty():
                color = self.RESET
                nocolor = self.RESET
                if icon == NoticeIcon:
                    color = self.color(self.BLUE, True)
                elif icon == WarningIcon:
                    color = self.color(self.YELLOW, True)
                elif icon == ErrorIcon:
                    color = self.color(self.RED, True)

                icon = '[' + color + icon + nocolor + '] '
        return icon

    def output(self, message, icon = NoIcon):
        """prints to stdout"""
        if icon and icon != NoIcon:
            icon = self.colorize_icon(icon)
        print icon + message


if __name__ == '__main__':

    printer = CliPrinter()

    printer.output('random!', NoIcon)
    printer.output('notice!', NoticeIcon)
    printer.output('warning!', WarningIcon)
    printer.output('error!', ErrorIcon)
