from PyQt5 import uic, QtCore, QtWidgets

class BindTopMenu(object):
    def bind(self):
        self.window.findChild(QtWidgets.QAction, 'openfile_top_menu').triggered.connect(self.open_automata_handler)
        self.window.findChild(QtWidgets.QAction, 'create_DFA_top_menu').triggered.connect(self.create_DFA_handler)
        self.window.findChild(QtWidgets.QAction, 'create_DFMA_top_menu').triggered.connect(self.create_DFMA_handler)