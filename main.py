import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from tkinter import Tk, filedialog

from SaveOpen import save_bin
from StartWindow import StartWindow
from OpenedAutomata import OpenedAutomata
from DFMAVisual import DFMAVisual
import DFAVisual
from CreateNewDFA import CreateNewDFA
from CreateNewDFMA import CreateNewDFMA
from dfa.DFA import DFA
from dfma.pda.dpda import receiver, createTransition

class MainWindow(QtCore.QObject):

    def __init__(self, ui_file, parent = None):
        super(MainWindow, self).__init__(parent)
        StartWindow.setupUI(self, MainWindow)
        self.window.show()

    def open_automata_handler(self):
        Tk().withdraw()
        fileName = filedialog.askopenfilename(initialdir = "/", title = "Select file", filetypes = (("DFA .dfa","*.dfa"), ("DFMA .dfma", "*.dfma"), ("All files","*.*")))
        if (fileName[len(fileName)-4:] == ".dfa"):
            OpenedAutomata.setupUI(self, MainWindow, fileName, "DFA")
        if (fileName[len(fileName)-5:] == ".dfma"):
            OpenedAutomata.setupUI(self, MainWindow, fileName, "DFMA")

    def create_DFA_handler(self):
        CreateNewDFA.setupUI(self, MainWindow)

    def create_DFMA_handler(self):
        CreateNewDFMA.setupUI(self, MainWindow)

    def start_visualization_DFMA_handler(self):
        self.word = self.window.findChild(QtWidgets.QTextEdit, 'word_input').toPlainText()
        DFMAVisual.setupUI(self, MainWindow, self.word)

    def start_visualization_DFA_handler(self):
        self.word = self.window.findChild(QtWidgets.QTextEdit, 'word_input').toPlainText()
        print(MainWindow.dfa.get_table())
        DFAVisual.VisualizeDFA(MainWindow.dfa, self.word)

    def addColumn(self):
        self.tableWidget.setColumnCount(self.tableWidget.columnCount() + 1)
    
    def addRow(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)

    def delColumn(self):
        self.tableWidget.setColumnCount(self.tableWidget.columnCount() - 1)
    
    def delRow(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() - 1)

    def saveNewDFA(self):
        Tk().withdraw()
        dirPath = filedialog.askdirectory()
        dirPath += '/automataDFA.dfa'
        table = list()
        i = self.tableWidget.columnCount()
        j = self.tableWidget.rowCount()
        for row in list(range(0, j)):
            symbols = list()
            for col in list(range(0, i)):
                try:
                    symbols.append(self.tableWidget.item(row, col).text())
                except:
                    symbols.append(' ')
            table.append(symbols)
        try: 
            dfa = DFA.table_parse(table)
            self.window.findChild(QtWidgets.QLabel, 'exeption_label').setText('Сохранен')
        except:
            self.window.findChild(QtWidgets.QLabel, 'exeption_label').setText('Ошибка создания автомата, проверьте правильность ввода данных')
        try: 
            save_bin(dfa, dirPath)
        except:
            self.window.findChild(QtWidgets.QLabel, 'exeption_label').setText('Ошибка схоранения')

    def saveNewDFMA(self):
        print(createTransition([['q0', 'a', 'q1', '0', ['1', '0']], ['q1', 'a', 'q1', '1', ['1', '1']], ['q1', 'b', 'q2', '1', ['']], ['q2', 'b', 'q2', '1', ['']], ['q2', 'e', 'q3', '0', ['0']]]
))
        Tk().withdraw()
        dirPath = filedialog.askdirectory()
        dirPath += '/automataDFMA.dfma'
        states = list()
        transitions = list()
        input_symbols = list()

        i = self.tableWidget.columnCount()
        j = self.tableWidget.rowCount()
        for row in (list(range(1, j))):
            transitionItem = list()
            state = self.tableWidget.item(row, 0).text()
            if state not in states:
                states.append(state)
            state = self.tableWidget.item(row, 3).text()
            if state not in states:
                states.append(state)
            symbol = self.tableWidget.item(row, 1).text()
            if symbol not in input_symbols:
                input_symbols.append(symbol)
            for col in (list(range(0, i))):
                if col == 4:
                    try:
                        transitionItem.append(self.tableWidget.item(row, col).text().split(' '))
                    except:
                        transitionItem.append('')

                else:
                    transitionItem.append(self.tableWidget.item(row, col).text())
            transitions.append(transitionItem)
        try:
            initial_state = self.window.findChild(QtWidgets.QTextEdit, 'initial_state_input').toPlainText()
            final_states = self.window.findChild(QtWidgets.QTextEdit, 'final_states_input').toPlainText()
            final_states = final_states.split(' ')
            stack_symbols = self.window.findChild(QtWidgets.QTextEdit, 'stack_symbols_input').toPlainText()
            stack_symbols = stack_symbols.split(' ')
            initial_stack_symbol = self.window.findChild(QtWidgets.QTextEdit, 'initial_stack_symbol_input').toPlainText()
        except:
            print('error')
        print(states)
        print(transitions)
        print(input_symbols)
        print(initial_state)
        print(final_states)
        print(stack_symbols)
        print(initial_stack_symbol)
        print(createTransition(transitions))
        dfma = receiver(
            states,
            transitions,
            input_symbols,
            initial_state,
            final_states,
            stack_symbols,
            initial_stack_symbol
        )
        save_bin(dfma, dirPath)




app = QtWidgets.QApplication(sys.argv)
form = MainWindow("./ui/main_window.ui")
sys.exit(app.exec_())