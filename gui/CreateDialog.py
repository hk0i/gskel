import os
import sys

from PySide.QtCore import *
from PySide.QtGui import *

from model.logger import log
from model import gskel
from model.language import Language, Languages
from model.project import Project
from model import skelfactory

class CreateDialog(QDialog):
    """docstring for CreateDialog"""
    def __init__(self, skel, parent = None):
        super(CreateDialog, self).__init__(parent)

        self.skel = skel
        args = skel.params

        if args and len(args) > 0:
            #if out skeleton requires parameters, set up the ui accordingly

            self.set_up_param_widgets(args)

            # self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.resize(400, 150)
            self.setMinimumWidth(300)
            self.show()
            self.raise_()
        else:
            #otherwise just get the output file name and generate
            output_file = QFileDialog.getSaveFileName(
                self,
                self.tr('Save as...')
            )

            if output_file[0]:
                self.create_project(output_file[0])

    def set_up_param_widgets(self, args):
        """Sets up UI widgets for gskel param input"""
        self.textfields = []
        formParams = QFormLayout()
        formParams.setHorizontalSpacing(15)
        formParams.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)

        layout = QVBoxLayout()
        self.txtOutput = QLineEdit(self.tr('File Path...'))
        self.tbOutput  = QPushButton(self.tr('...'))

        hboxOutput = QHBoxLayout()
        hboxOutput.addWidget(self.txtOutput)
        hboxOutput.addWidget(self.tbOutput)
        formParams.addRow(QLabel(self.tr('Output path')), hboxOutput)

        for arg in args:

            #well, if it .keys() like a dict...
            try:
                param = arg.keys()[0]
            except AttributeError:
                param = arg

            label = QLabel(param.lower())
            le = QLineEdit(param, self)
            # le.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            self.textfields.append(le)

            formParams.addRow(label, le)

        layout.addItem(formParams)

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

        # self.show()
        # self.raise_()

    def widgets_to_params(self):
        """Takes all params from widgets and throws it into a list"""
        args = []
        for textfield in self.textfields:
            args.append(textfield.text())

        return args

    def create_project(self, output_path, args = []):
        """creates the project files"""
        project = Project(
            name = 'Default Project',
            skel = self.skel,
            params = args
        )

        project.create_files(output_path)
        self.parent().trayIcon.showMessage(
            self.tr('qgskel'),
            self.tr('Files created')
        )

    @Slot()
    def accepted(self):
        """ok clicked"""
        self.create_project(self.txtOutput.text(), self.widgets_to_params())
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
            self.tr('Select output path'),
            options = QFileDialog.ShowDirsOnly
        )

        if directory:
            self.txtOutput.setText(directory)

if __name__ == '__main__':
    qapp = QApplication(sys.argv)
    c = CreateDialog(['testing', 'this', 'out'], None)
    sys.exit(qapp.exec_())


