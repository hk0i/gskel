import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

# from model.logger import log
# from model import gskel
# from model.language import Language, Languages
# from model.project import Project
# from model import skelfactory

class CreateDialog(QDialog):
    """docstring for CreateDialog"""
    def __init__(self, args, parent = None):
        super(CreateDialog, self).__init__(parent)

        if args and len(args) > 0:
            textfields = []
            layout = QVBoxLayout()
            self.txtOutput = QLineEdit(self.tr('File Path...'))
            self.tbOutput  = QPushButton(self.tr('...'))

            hboxOutput = QHBoxLayout()
            hboxOutput.addWidget(self.txtOutput)
            hboxOutput.addWidget(self.tbOutput)
            layout.addItem(hboxOutput)

            for arg in args:
                print 'arg:', arg

                #well, if it .keys() like a dict...
                try:
                    param = arg.keys()[0]
                except AttributeError:
                    param = arg

                le = QLineEdit(param, self)
                textfields.append(le)
                layout.addWidget(le)
            layout.addStretch()
            self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                    QDialogButtonBox.Cancel)
            layout.addWidget(self.buttonBox)

            self.setLayout(layout)
            # textfields[0].setSelection(0, len(textfields[0].text()))

            #set up connections
            self.tbOutput.clicked.connect(self.save_as)
            self.buttonBox.accepted.connect(self.accepted)
            self.buttonBox.rejected.connect(self.rejected)

        self.resize(200, 200)

    @Slot()
    def accepted(self):
        """ok clicked"""
        self.close()

    @Slot()
    def rejected(self):
        """cancel clicked"""
        self.close()

    @Slot()
    def save_as(self):
        """Open save file dialog"""
        directory = QFileDialog.getExistingDirectory(
            self,
            self.tr('Select output path')
        )

        if directory:
            self.txtOutput.setText(directory)

if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    c = CreateDialog(['testing', 'this', 'out'], None)
    sys.exit(qapp.exec_())


