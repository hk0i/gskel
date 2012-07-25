from PySide.QtGui import *

from model.gsprinter import GSPrinter

Printer = 'qt_tray'

NoIcon = QSystemTrayIcon.NoIcon
NoticeIcon = QSystemTrayIcon.Information
WarningIcon = QSystemTrayIcon.Warning
ErrorIcon = QSystemTrayIcon.Critical

class TrayPrinter(GSPrinter):
    """docstring for TrayPtine"""
    def __init__(self, trayIcon):

        self.trayIcon = trayIcon

        #need to find a better way to do this...
        self.NoIcon = NoIcon
        self.NoticeIcon = NoticeIcon
        self.WarningIcon = WarningIcon
        self.ErrorIcon = ErrorIcon


    def output(self, message, icon = NoIcon):
        """displays a message using QSystemTrayIcon"""
        print 'TrayPrinter.output -- ', message
        self.trayIcon.showMessage('qgskel', message, icon)

