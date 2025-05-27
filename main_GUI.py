import sys,os  
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot,pyqtProperty,QObject
import numpy as np
import datetime,time
from queue import Queue
from collections import namedtuple as nmd


# from pyqtgraph.Qt import QtCore, QtGui
# import pyqtgraph as pg
# import pyqtgraph.console
# from pyqtgraph.parametertree import Parameter, ParameterTree

import design_works_qs3 as design
# import design
import queue_data_classes

class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self,ques,args):
        super().__init__()
        self.calib_dat=queue_data_classes.calib_input_data()
        self.fft_dat=queue_data_classes.FFT_input_data(self.calib_dat.scope_IP) 
        self.setupUi(self)
        #self.fileName = fileName
        self.model = QtGui.QStandardItemModel(self) 
        self.ques=ques
        self.args=args
        # time.sleep(1)
        # self.timer.timeout.connect(lambda: self.update_from_qus())
        # self.timer.start(10000)       

def main(ques,args=0):
    print("Hi alla")
    print(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    window = App(ques,args)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()