import sys,os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot,pyqtProperty

import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

import pyqtgraph.console
from pyqtgraph.parametertree import Parameter, ParameterTree

class App(QtGui.QMainWindow):

    def help(self):
        print('Use this console to execute commands in context of application')

    # def rpc(self,f,*arg):
    #     return self.controlWidget.client.call(f,*arg) 
    
    def __init__(self):
        super().__init__()
        self.title = 'Starta GUI'
        # self.left = 10
        # self.top = 10
        # self.width = 320
        # self.height = 100
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()

    # def __init__(self,app=None):
    #     super().__init__()
    #     self.setWindowTitle(f'Oryx GUI')    
    #     if app:
    #         app.aboutToQuit.connect(self.closeAll)          

        # Initialize tab screen
        self.tabs = QtGui.QTabWidget()
        self.fft_tab = QtGui.QWidget()
        self.calib_tab = QtGui.QWidget()

        # Add tabs
        self.tabs.addTab(self.fft_tab,"FFT Tab")
        self.tabs.addTab(self.calib_tab,"Calib Tab")

        # Create first tab
        self.fft_tab.layout = QtGui.QVBoxLayout(self)
        self.pushButton1 = QtGui.QPushButton("Set input")
        self.fft_tab.layout.addWidget(self.pushButton1)
        self.fft_tab.setLayout(self.fft_tab.layout)
        
        # Create second tab        
        self.col = QColor(0, 0, 0)

        self.main_layout = QtGui.QHBoxLayout()
          
        self.main_layout.addWidget(self.tabs)
        self.main_layout.setStretch(0,90)       
        self.main_layout.setStretch(1,0)
        
        self.setCentralWidget(QtGui.QWidget())
        self.centralWidget().setLayout(self.main_layout)
        
        #self.setLayout(vbox_layout)

        self.calib_tab.layout = QtGui.QVBoxLayout(self)
        self.linear = QtGui.QPushButton("Linearization")
        self.linear.setCheckable(True)
        #self.linear.move(10, 10)
        self.linear.clicked[bool].connect(self.setGraph)
        self.calib_tab.layout.addWidget(self.linear)
        self.calib_tab.setLayout(self.calib_tab.layout)       

        self.flat = QtGui.QPushButton("Cumsum flattening")
        self.flat.setCheckable(True)
        #self.flat.move(10, 60)
        self.flat.clicked[bool].connect(self.setGraph)
        self.calib_tab.layout.addWidget(self.flat)
        self.calib_tab.setLayout(self.calib_tab.layout)  

        self.calib = QtGui.QPushButton("Chip calib")
        self.calib.setCheckable(True)
        #self.calib.move(10, 110)
        self.calib.clicked[bool].connect(self.setGraph)
        self.calib_tab.layout.addWidget(self.calib)
        self.calib_tab.setLayout(self.calib_tab.layout)     

        # Create grid layout
        # grid_layout = QtGui.QGridLayout()
        # vbox_layout = QtGui.QVBoxLayout()
        # vbox_layout.addLayout(grid_layout)
        
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Calib")
        layout = QGridLayout()
        layout.setColumnStretch(1, 6)
        layout.setColumnStretch(2, 6)

        self.square =QtGui.QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
            self.col.name())

        #self.button_set.clicked.connect(lambda:self.on_set())

        # Create labels & textboxes
        self.label = layout.addWidget(QtGui.QLabel('linearization: # iterations'),1,0)
        #self.label.move(200,40)
        #self.calib_tab.layout.addWidget(self.label)
        self.calib_tab.setLayout(self.calib_tab.layout)

        self.textbox1 = layout.addWidget(QtGui.QLineEdit(self),1,1)
        #self.textbox1.move(200, 60)
        #self.textbox1.resize(280,40)
        #self.calib_tab.layout.addWidget(self.textbox1)
        self.calib_tab.setLayout(self.calib_tab.layout)

        self.labe2 = layout.addWidget(QtGui.QLabel('flattening: Vstart, Kp, Ki, Kd'),1,2)
        #self.labe2.move(200,90)
        #self.calib_tab.layout.addWidget(self.labe2)
        self.calib_tab.setLayout(self.calib_tab.layout)

        self.textbox2 = layout.addWidget(QtGui.QLineEdit(self),1,3)
        #self.textbox2.move(200, 110)
        #self.textbox2.resize(280,40)
        #self.calib_tab.layout.addWidget(self.textbox2)
        self.calib_tab.setLayout(self.calib_tab.layout)

        self.labe3 = layout.addWidget(QtGui.QLabel('Chip calib: amp_attenuation'),1,4)
        #self.labe3.move(200,130)
        #self.calib_tab.layout.addWidget(self.labe3)
        self.calib_tab.setLayout(self.calib_tab.layout)

        self.textbox3 = layout.addWidget(QtGui.QLineEdit(self),1,5)
        #self.textbox3.move(200, 140)
        #self.textbox3.resize(280,40)
        #self.calib_tab.layout.addWidget(self.textbox3)
        self.calib_tab.setLayout(self.calib_tab.layout)

        self.setinput2 = layout.addWidget(QtGui.QPushButton("Set input"),1,6)
        #self.setinput2.setCheckable(True)
        #self.setinput2.move(200, 200)
        #self.calib_tab.layout.addWidget(self.setinput2)
        self.calib_tab.setLayout(self.calib_tab.layout)

        self.horizontalGroupBox.setLayout(layout)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Starta GUI')
        self.show()
        self.resize(1100,600)
    
    def setGraph(self, pressed):

        source = self.sender()

        if pressed:
            val = 255
        else: val = 0

        if source.text() == "Linearization":
            self.col.setRed(val)
        elif source.text() == "Cumsum flattening":
            self.col.setGreen(val)
        elif source.text() == "Chip calib":
            self.col.setBlue(val)            
        #else:
        #    self.col.setBlue(val)

        self.square.setStyleSheet("QFrame { background-color: %s }" %
            self.col.name())    
        
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())