from PyQt5 import uic, QtCore, QtWidgets, Qt
from dfma.pda.dpda import DPDA
from BindTopMenu import BindTopMenu

class DFMAVisual(object):
    def setupUI(self, MainWindow, word):
        result = MainWindow.dfma.read_input(word)

        ui_file = QtCore.QFile("./ui/dfma_visual.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        self.window = uic.loadUi(ui_file)
        ui_file.close()
        BindTopMenu.bind(self)
        self.window.findChild(QtWidgets.QLabel, 'automata_name').setText("DFMA")
        tableWidget = QtWidgets.QTableWidget()
        tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        tableWidget.setColumnWidth(1, 100)
        tableWidget.setRowCount(len(result))
        tableWidget.setColumnCount(3)
        tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("МАГАЗИН"))
        tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem("СОСТОЯНИЕ"))
        tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem("ВХОДНАЯ ЛЕНТА"))
        
        i = -1
        for x in result:
            i += 1
            if x[0][0] == 'q':
                tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(''.join(x[0])))
                tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(''.join(x[1])))
                tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(''.join(x[2])))
            try:
                if x.find("dfma.base.exceptions.RejectionException") != -1:
                    tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem("Автомат завершил работу с ошибкой"))
                    tableWidget.setSpan(i, 0, 1, 3)
            except: 
                continue
        
        self.window.findChild(QtWidgets.QLayout, 'table_automata_vizual').addWidget(tableWidget)

        self.window.show()