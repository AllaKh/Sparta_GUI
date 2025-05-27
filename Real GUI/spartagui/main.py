import sys,os  
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot,pyqtProperty,QObject
import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.console
from pyqtgraph.parametertree import Parameter, ParameterTree

import design

class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()