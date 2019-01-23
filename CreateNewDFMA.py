from PyQt5 import uic, QtCore, QtWidgets, Qt
from BindTopMenu import BindTopMenu

class CreateNewDFMA(object):
    def setupUI(self, MainWindow):
        ui_file = QtCore.QFile("./ui/create_dfma.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.window = uic.loadUi(ui_file)
        ui_file.close()
        BindTopMenu.bind(self)
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.tableWidget.setColumnWidth(1, 100)
        self.tableWidget.setRowCount(2)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Из  состояния"))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("По символу"))
        self.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem("Вершина стека"))
        self.tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem("В сосотояние"))
        self.tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem("Добавить в стек"))

        self.window.findChild(QtWidgets.QPushButton, 'add_row').clicked.connect(self.addRow)
        self.window.findChild(QtWidgets.QPushButton, 'del_row').clicked.connect(self.delRow)
        
        self.window.findChild(QtWidgets.QPushButton, 'save_new_dfma').clicked.connect(self.saveNewDFMA)
        
        self.window.findChild(QtWidgets.QLayout, 'table_layout_new_dfma').addWidget(self.tableWidget)
        self.window.show()