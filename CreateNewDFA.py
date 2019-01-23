from PyQt5 import uic, QtCore, QtWidgets, Qt
from BindTopMenu import BindTopMenu

class CreateNewDFA(object):
    def setupUI(self, MainWindow):
        ui_file = QtCore.QFile("./ui/create_dfa.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.window = uic.loadUi(ui_file)
        ui_file.close()
        BindTopMenu.bind(self)
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(1)
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("_"))

        self.window.findChild(QtWidgets.QPushButton, 'add_column').clicked.connect(self.addColumn)
        self.window.findChild(QtWidgets.QPushButton, 'add_row').clicked.connect(self.addRow)
        self.window.findChild(QtWidgets.QPushButton, 'del_column').clicked.connect(self.delColumn)
        self.window.findChild(QtWidgets.QPushButton, 'del_row').clicked.connect(self.delRow)
        self.window.findChild(QtWidgets.QPushButton, 'save_new_dfa').clicked.connect(self.saveNewDFA)
        
        self.window.findChild(QtWidgets.QLayout, 'table_layout_new_dfa').addWidget(self.tableWidget)
        self.window.show()