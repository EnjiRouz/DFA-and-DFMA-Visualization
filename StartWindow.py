import sys
from PyQt5 import uic, QtCore, QtWidgets
from BindTopMenu import BindTopMenu

class StartWindow(object):
    def setupUI(self, MainWindow):
        ui_file = QtCore.QFile("./ui/main_window.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.window = uic.loadUi(ui_file)
        ui_file.close()
        BindTopMenu.bind(self)
        self.window.findChild(QtWidgets.QPushButton, 'open_automata').clicked.connect(self.open_automata_handler)
        self.window.findChild(QtWidgets.QPushButton, 'create_DFA_button').clicked.connect(self.create_DFA_handler)
        self.window.findChild(QtWidgets.QPushButton, 'create_DFMA_button').clicked.connect(self.create_DFMA_handler)
        self.window.show()