import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

from model.logger import log
from model import gskel
from model.language import Language, Languages
from model.project import Project
from model import skelfactory

from gui.CreateDialog import *


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
                        skel.params,
                        parent = self.parent()
                    )
                    createDialog.show()
                    # self.parent().show()
                    # project = Project(
                        # name = 'Default Project',
                        # skel = skel,
                        # params = None
                    # )
                    for param in skel.params:
                        print param
                    # project.create_files(output_file)

                    print 'Okay!', directive
                    break

    def closeEvent(self, event):
        """Stop exiting when we close the dialog"""

        print 'Close event!!! CreateDialog!!!'
        self.reject()
        event.ignore()



        print directiveName, self.parent().langs

class ProjectMenu(QWidget):
    """Main menu for working with gskel projects"""

    def __init__(self, parent = None):
        super(ProjectMenu, self).__init__(parent)

        log.debug('Initializing tray icon...')
        self.menuListener = MenuListener(self)

        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.setIcon(QIcon('/Users/gmcquillan/apps/gskel/Skull_256.png'))

        self.setWindowTitle('gskel gui')
        self.create_menu()

        self.trayIcon.show()

    def create_menu_actions(self):
        """ creates actions for menus """

        # self.newMenu = QAction(
            # self.tr('&New'),
            # self
        # )

        self.quitAction = QAction(
            self.tr('&Quit'),
            self,
            triggered = QApplication.quit
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

        # self.trayMenu.addAction(self.newMenu)
        # self.trayMenu.addSeparator()
        self.create_dynamic_menu()
        self.trayMenu.addSeparator()
        self.trayMenu.addAction(self.quitAction)

        self.trayIcon.setContextMenu(self.trayMenu)

    def newClicked(self):
        """ triggered on menu click of new > lang > directive """
        menuItem = QObject.sender()
        emit(self.createNew(menuItem.text()))
