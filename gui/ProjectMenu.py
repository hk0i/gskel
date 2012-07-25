import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

from model import logger
from model import gskel
from model.language import Language, Languages
from model.project import Project
from model import skelfactory

from gui.CreateDialog import *
from gui.TrayPrinter import *

VERSION = '1.0b'

class MenuListener(QObject):
    """ Fulfuls dynamic menu requests """
    def __init(self, parent = None):
        super(MenuListener, self).__init__(parent)
        self.parent = parent

    @Slot()
    def on_click(self, *args):
        mnu = self.sender()
        self.create_skeleton(mnu.text().split('New')[1].strip())

    def create_skeleton(self, directiveName):
        """ creates skeleton from directive full name """
        langs = self.parent().langs
        for lang in langs.languages:
            for directive in lang.directives:
                k = directive.keys()[0]
                skel = skelfactory.create_skel(directive[k])
                if skel.name == directiveName:
                    createDialog = CreateDialog(
                        skel,
                        parent = self.parent()
                    )
                    createDialog.setWindowTitle('[gskel] New ' + directiveName + '...')
                    break

class ProjectMenu(QWidget):
    """Main menu for working with gskel projects"""

    def __init__(self, parent = None):
        super(ProjectMenu, self).__init__(parent)

        self.trayIcon = QSystemTrayIcon()

        self.menuListener = MenuListener(self)

        self.icon = QIcon('/Users/gmcquillan/apps/gskel/Skull_256.png')
        self.setWindowIcon(self.icon)
        self.trayIcon.setIcon(self.icon)

        self.setWindowTitle('gskel gui')
        self.create_menu()

        self.trayIcon.show()

        logger.log = logger.Logger(printer = TrayPrinter(self.trayIcon))
        logger.log.notice('Test error!')
    def create_menu_actions(self):
        """ creates actions for menus """

        self.quitAction = QAction(
            self.tr('&Quit'),
            self,
            triggered = QApplication.quit
        )

        self.aboutAction = QAction(
            self.tr('&About qgskel...'),
            self,
            triggered = self.show_about
        )

        self.aboutQtAction = QAction(
            self.tr('&About Qt...'),
            self,
            triggered = lambda: QMessageBox.aboutQt(self)
        )

    def create_dynamic_menu(self):
        """creates dynamic menu for skeleton creation"""

        self.langs = Languages(os.path.join(sys.path[0], 'skel/language.xml'))
        self.langs.load_directives(os.path.join(sys.path[0], 'skel'))
        for lang in self.langs.languages:
            nuLang = QMenu(
                self.tr(str(lang))
            )

            for directive in lang.directives:
                k = directive.keys()[0]
                skel = skelfactory.create_skel(directive[k])
                if skel.name:
                    nuDir = QAction(
                        self.tr('New ' + skel.name),
                        self,
                    )

                    nuDir.triggered.connect(self.menuListener.on_click)

                    nuLang.addAction(nuDir)

            self.trayMenu.addMenu(nuLang)

    def create_menu(self):
        """ creates systray icon """

        log.debug('Initializing tray icon menu...')
        self.create_menu_actions()

        self.trayMenu = QMenu(self)

        self.trayMenu.addAction(self.aboutAction)
        self.trayMenu.addAction(self.aboutQtAction)
        self.trayMenu.addSeparator()

        self.create_dynamic_menu()
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(self.quitAction)

        self.trayIcon.setContextMenu(self.trayMenu)

    def newClicked(self):
        """ triggered on menu click of new > lang > directive """
        menuItem = QObject.sender()
        emit(self.createNew(menuItem.text()))

    def show_about(self):
        about = QMessageBox(self)

        about.setIconPixmap(self.icon.pixmap(128, 128))
        about.setWindowTitle('qgskel')
        about.setTextFormat(Qt.RichText)
        about.setText(
            self.tr(
                '<h1>qgskel</h1> project skeleton creator gui in Qt<br/>'
                'GUI Version: %s<br/>'
                'gskel (library) version: %s<br/><br/>'
                'Written by: Gregory McQuillan<br/>'
                'Available from source: '
                "<a href='http://github.com/hk0i/gskel'>http://github.com/hk0i/gskel</a>"
                % (VERSION, gskel.VERSION)
            )
        )

        about.exec_()
        about.raise_()

