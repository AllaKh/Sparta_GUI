import sys,os  
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import *
import numpy as np
import datetime,time
#import design_old as design
import design_trys as design
import queue_data_classes_offline as queue_data_classes


class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.calib_dat=queue_data_classes.calib_input_data()
        self.fft_dat=queue_data_classes.FFT_input_data() 
        self.setupUi(self)
        #self.fileName = fileName
        self.model = QtGui.QStandardItemModel(self)         

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()