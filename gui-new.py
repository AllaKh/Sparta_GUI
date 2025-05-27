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
    def __init__(self,app=None):
        super().__init__()
        self.setWindowTitle('Oryx GUI')   

        self.controlWidget=ControlWidget(self)
        #self.setCentralWidget(self.tabs)
        # self.main_layout = QtGui.QHBoxLayout()     
        
        self.controlWidget=ControlWidget()
        
        # Initialize tab screen
        self.tabs = QtGui.QTabWidget()
        self.fft_tab = QtGui.QWidget()
        self.calib_tab = QtGui.QWidget()

        # Add tabs
        self.tabs.addTab(self.fft_tab,"FFT Tab")
        self.tabs.addTab(self.calib_tab,"Calib Tab")    
        
        self.main_layout = QtGui.QHBoxLayout()
        
        
        self.main_layout.addWidget(self.tabs)
        self.main_layout.addWidget( self.controlWidget )
        self.main_layout.setStretch(0,90)       
        self.main_layout.setStretch(1,0)
        

        self.setCentralWidget( QtGui.QWidget())
        self.centralWidget().setLayout(self.main_layout)
        self.show()
        self.resize(1100,600)
  

        #self.setCentralWidget(QtGui.QWidget())
        #self.centralWidget().setLayout(self.main_layout)
        self.show()
        self.resize(1100,600)
    
class ControlWidget(QtGui.QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        
        # # Initialize tab screen
        # self.tabs = QtGui.QTabWidget()
        # self.fft_tab = QtGui.QWidget()
        # self.calib_tab = QtGui.QWidget()

        # # Add tabs
        # self.tabs.addTab(self.fft_tab,"FFT Tab")
        # self.tabs.addTab(self.calib_tab,"Calib Tab")
        
        # self.main_layout = QtGui.QHBoxLayout()     
        
        # self.main_layout.addWidget(self.tabs)
        # #self.main_layout.addWidget(self.controlWidget)
        # self.main_layout.setStretch(0,90)       
        # self.main_layout.setStretch(1,0)  

        # Create grid layout
        #self.layout = QVBoxLayout(self)
        #layout = QtGui.QGridLayout()
        # vbox_layout = QtGui.QVBoxLayout()
        # vbox_layout.addLayout(layout)
        
        # self.setLayout(vbox_layout)

        # self.horizontalGroupBox = QGroupBox("Calib")
        # layout = QGridLayout()
        # layout.setColumnStretch(1, 6)
        # layout.setColumnStretch(2, 6)

        # self.square =QtGui.QFrame(self)
        # self.square.setGeometry(150, 20, 100, 100)
        # self.square.setStyleSheet("QWidget { background-color: %s }" %
        #     self.col.name())

        # Create first tab
        self.fft_tab.layout = QtGui.QVBoxLayout(self)
        self.pushButton1 = QtGui.QPushButton("Set input")
        self.fft_tab.layout.addWidget(self.pushButton1)
        self.fft_tab.setLayout(self.fft_tab.layout)

        # Create second tab 
        self.col = QColor(0, 0, 0)

        grid_layout = QtGui.QGridLayout()
        vbox_layout = QtGui.QVBoxLayout()
        vbox_layout.addLayout(grid_layout)
        
        self.setLayout(vbox_layout)


        self.calib_tab.layout = QtGui.QVBoxLayout(self)
        self.linear = QtGui.QPushButton("Linearization")
        self.linear.setCheckable(True)
        #self.linear.move(10, 10)
        self.linear.clicked[bool].connect(self.setGraph)
        # layoutaddWidget(self.linear)
        # self.calib_tab.setLayout(self.layout)       

        self.flat = QtGui.QPushButton("Cumsum flattening")
        self.flat.setCheckable(True)
        #self.flat.move(10, 60)
        self.flat.clicked[bool].connect(self.setGraph)
        # layoutaddWidget(self.flat)
        # self.calib_tab.setLayout(self.layout)  

        self.calib = QtGui.QPushButton("Chip calib")
        self.calib.setCheckable(True)
        #self.calib.move(10, 110)
        self.calib.clicked[bool].connect(self.setGraph)
        # layoutaddWidget(self.calib)
        # self.calib_tab.setLayout(self.layout)    

        # Create labels & textboxes
        self.label1 = QtGui.QLabel('linearization: # iterations')
        self.label1.setMaximumWidth(100)
        self.label1.setFixedWidth(100)
        self.textbox1 = QtGui.QLineEdit("# linearization iterations")
        self.textbox1.setMaximumWidth(100)
        self.textbox1.setFixedWidth(100)

        self.label2 = QtGui.QLabel('flattening: Vstart, Kp, Ki, Kd')
        self.label2.setMaximumWidth(100)
        self.label2.setFixedWidth(100)
        self.textbox2 = QtGui.QLineEdit("Flatten_params (=[4x1 numpy])")
        self.textbox1.setMaximumWidth(100)
        self.textbox1.setFixedWidth(100)

        self.label3 = QtGui.QLabel('Chip calib: amp_attenuation')
        self.label3.setMaximumWidth(100)
        self.label3.setFixedWidth(100)
        self.textbox3 = QtGui.QLineEdit("chip_params (=1 numpy)")
        self.textbox3.setMaximumWidth(100)
        self.textbox3.setFixedWidth(100)

        self.button_set2 = QtGui.QPushButton("Set input")       
        self.button_set2.setMaximumWidth(100)
        self.button_set2.setFixedWidth(100)        
        
        # self.button_connect.clicked.connect(lambda:self.on_connect())
        # self.button_start.clicked.connect(lambda:self.on_start())
        # self.button_stop.clicked.connect(lambda:self.on_stop())

        layout.addWidget(self.linear,0,0)
        #self.calib_tab.setLayout(self.layout) 
        layout.addWidget(self.flat,0,1)
        #self.calib_tab.setLayout(self.layout)
        layout.addWidget(self.calib,0,2)
        #self.calib_tab.setLayout(self.layout)
        layout.addWidget(self.label1,1,0)
        #self.calib_tab.setLayout(self.layout)
        layout.addWidget(self.textbox1,1,1)
        #self.calib_tab.setLayout(self.layout)               
        layout.addWidget(self.label2,1,2)
        #self.calib_tab.setLayout(self.layout)
        layout.addWidget(self.textbox2,1,3)
        #self.calib_tab.setLayout(self.layout) 
        layout.addWidget(self.label3,1,4)
        #self.calib_tab.setLayout(self.layout)
        layout.addWidget(self.textbox3,1,5)
        #self.calib_tab.setLayout(self.layout) 
        layout.addWidget(self.button_set2,1,6)
        #self.calib_tab.setLayout(self.layout)
        # layout.addWidget(self.button_stop,1,1)
        # layout.addWidget(QtGui.QLabel("CTRL version"),2,0)
        # layout.addWidget(self.ctrl_ver,2,1)
        # layout.addWidget(QtGui.QLabel("FPGA version"),3,0)
        # layout.addWidget(self.fpga_ver,3,1)
        #layout.addWidget(self.t,10,0,2,2)
        
        spacer = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        layout.addItem(spacer)

        self.client=None

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

def start(args):
    
    app=    QtGui.QApplication([])
    app.setStyle('Windows')
    gui = App(app)
    app.instance().exec_()


if __name__ == '__main__':
    start(None) 
        
