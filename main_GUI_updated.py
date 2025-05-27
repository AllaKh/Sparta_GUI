###############################################################################
#                              file: main_GUI.py                              #
#                                                                             #
# 	author: Alla Khananashvili                                                #
# 	date: Aug-12-2019                                                         #
#                                                                             #
# 	version: 8.0                                                              #
# 	python version: 3.6	                                                      #
#                                                                             #
#   Description:                                                              #
#   Run multithreading GUI which gets parameters from queues and updates      #
#   text fields and graphs on startup, then checks for the queue updates      #
#   and updates graphs in real time.                                          #
#   Uses for FFT monitoring and laser Calibration                             #
#   While calibration process runs nothing can be send to the queue.          #
#                                                                             #
###############################################################################

#Import Python libraries
import sys,os  
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot,pyqtProperty,QObject
import numpy as np
import datetime,time
from queue import Queue
from collections import namedtuple as nmd

#Import design script
import design_works_qs3 as design
# import design
import queue_data_classes

#Define threads for run
class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self,ques,args):
        # Accsess to the variables, methods, etc. in design.py file
        super().__init__()
        # Queues definition
        self.calib_dat=queue_data_classes.calib_input_data()
        self.fft_dat=queue_data_classes.FFT_input_data(self.calib_dat.scope_IP)         
        self.setupUi(self) #Design initiation
        self.model = QtGui.QStandardItemModel(self) 
        self.ques=ques
        self.args=args

#Run GUI window
def main(ques,args=0):
    print("Hi Alla")
    print(sys.argv)
    app = QtWidgets.QApplication(sys.argv) # A new copy of QApplication
    window = App(ques,args) # Creation of object in class App
    window.show() #Show the window
    app.exec_() #Run the application

if __name__ == '__main__':
    main() #Run main function