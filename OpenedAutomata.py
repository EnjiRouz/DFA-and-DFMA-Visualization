from PyQt5 import uic, QtCore, QtWidgets
from SaveOpen import read_from_bin as openAutomata
from dfa.DFA import DFA
from dfma.pda.dpda import DPDA
from BindTopMenu import BindTopMenu
from SaveOpen import read_from_bin

class OpenedAutomata(object):
    def setupUI(self, MainWindow, fileName, automataType):
        ui_file = QtCore.QFile("./ui/opened_automata.ui")
        ui_file.open(QtCore.QFile.ReadOnly)
        
        self.window = uic.loadUi(ui_file)
        ui_file.close()
        BindTopMenu.bind(self)
        self.window.findChild(QtWidgets.QLabel, 'automata_name').setText(automataType)
        tableWidget = QtWidgets.QTableWidget()

        self.window.findChild(QtWidgets.QAction, 'openfile_top_menu').triggered.connect(self.open_automata_handler)
        self.window.findChild(QtWidgets.QAction, 'create_DFA_top_menu').triggered.connect(self.open_automata_handler)
        self.window.findChild(QtWidgets.QAction, 'create_DFMA_top_menu').triggered.connect(self.open_automata_handler)

        visualization = self.window.findChild(QtWidgets.QPushButton, 'start_vizualization')
        # DFMA vizualization
        if (automataType == 'DFMA'):
            tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
            tableWidget.setColumnWidth(1, 100)
            MainWindow.dfma = DPDA( states={'q0', 'q1', 'q2', 'q3'}, 
            input_symbols={'a', 'b'}, 
            stack_symbols={'0', 'A', 'B'}, 
            transitions={ 
            'q0': { 'a': {'0': ('q0', ('A', '0')), 'A': ('q0', ('A', 'A'))},
                
                    'b': {'A': ('q1', '')},
             }, 
            
            'q1': { 'a': {'0': ('q2', ('B', '0'))}, 
                    'b': {'A': ('q1', '')} }, 

            'q2': { 'a': {'B': ('q2', ('B', 'B'))}, 
                    'b': {'B': ('q2', '')}, 
                    '': {'0': ('q3', ('0',))} } }, 
            initial_state='q0', 
            initial_stack_symbol='0', 
            final_states={'q3'} )
            alphabet = ''
            for liter in MainWindow.dfma.get_alphabet():
                alphabet += liter
                alphabet += ', '
            alphabet = alphabet[:-2]
            self.window.findChild(QtWidgets.QLabel, 'alphabet').setText(alphabet)
            table = MainWindow.dfma.get_table()
            tableWidget.setColumnCount(5)
            tableWidget.setRowCount(len(table) + 1)
            tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem('Из состояния'))
            tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem('По символу'))
            tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem('Вершина стека'))
            tableWidget.setItem(0, 3, QtWidgets.QTableWidgetItem('Добавить в стек'))
            tableWidget.setItem(0, 4, QtWidgets.QTableWidgetItem('В состояние'))
            i = 0
            for row in table:
                i += 1
                j = -1
                for item in row:
                    j += 1
                    tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(item)))
            visualization.clicked.connect(self.start_visualization_DFMA_handler)
        # DFA vizualization
        if (automataType == 'DFA'):
            MainWindow.dfa = read_from_bin(fileName)
            i = -1
            table = MainWindow.dfa.get_table()
            print(table)
            alphabet = ''
            for liter in table[0]:
                if (liter == '_'):
                    continue
                alphabet += liter
                alphabet += ', '
            alphabet = alphabet[:-2]
            self.window.findChild(QtWidgets.QLabel, 'alphabet').setText(alphabet)
            tableWidget.setRowCount(len(table))
            tableWidget.setColumnCount(len(table[0]))
            for row in table:
                i += 1
                j = -1
                for item in row:
                    j += 1
                    element = str(item).replace('[', '')
                    element = element.replace(']', '')
                    element = element.replace('\'', '')
                    tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(element))
            visualization.clicked.connect(self.start_visualization_DFA_handler)

        self.window.findChild(QtWidgets.QLayout, 'table_layout').addWidget(tableWidget)

        self.window.show()