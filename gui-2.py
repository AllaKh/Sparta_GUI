import sys,os

import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtProperty
from PyQt5 import QtCore, QtWidgets

class ControlWidget(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QtGui.QGridLayout()
        vbox_layout = QtGui.QVBoxLayout()
        vbox_layout.addLayout(layout)
        
        self.setLayout(vbox_layout)

        # self.button_linear = QtGui.QPushButton("Linearization")
        # self.button_flat = QtGui.QPushButton("Cumsum flattening")
        # self.button_calib = QtGui.QPushButton("Chip calib")
        # self.button_set   = QtGui.QPushButton("Set input")
        # self.button_stop    = QtGui.QPushButton("Stop")
        # self.ctrl_ip        = QtGui.QLineEdit("127.0.0.1")
        # self.ctrl_ver       = QtGui.QLineEdit("---",readOnly=True)
        # self.fpga_ver       = QtGui.QLineEdit("---",readOnly=True)
        # self.ctrl_ip.setMaximumWidth(100)
        # self.ctrl_ip.setFixedWidth(100)
        # self.button_connect.setMaximumWidth(100)
        # self.button_connect.setFixedWidth(100)
        #text_connect.setFixedWidth(200)
        
        # self.button_linear.clicked.connect(lambda:self.on_linear())
        # self.button_flat.clicked.connect(lambda:self.on_flat())
        # self.button_calib.clicked.connect(lambda:self.on_calib())

        #layout.addWidget(self.ctrl_ip,0,0)
        # layout.addWidget(self.button_linear,0,0)
        # layout.addWidget(self.button_flat,1,0)
        # layout.addWidget(self.button_calib,2,0)
        # layout.addWidget(QtGui.QLabel("linearization: # iterations"),0.1)
        # layout.addWidget(self.QLineEdit,1,1)
        # layout.addWidget(QtGui.QLabel("flattening: Vstart, Kp, Ki, Kd"),1,2)
        # layout.addWidget(self.QLineEdit,1,3)
        # layout.addWidget(QtGui.QLabel("Chip calib: amp_attenuation"),1,4)
        # layout.addWidget(self.QLineEdit,1,5)
        # layout.addWidget(self.button_set,1,6)      
        # self.lcd= QtGui.QLCDNumber(5)
        # self.lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        # layout.addWidget(self.lcd,4,0,4,4)
        
        spacer = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        layout.addItem(spacer)

        # Add tabs to widget
        #self.layout.addWidget(self.tabs)
        #self.setLayout(self.layout)

        self.client=None
       
class App(QtGui.QMainWindow):
   
    def __init__(self,app=None):
        super().__init__()
        self.setWindowTitle('Sparta GUI')    
        if app:
            app.aboutToQuit.connect(self.closeAll)
        
        #self.setWindowTitle(self.title)
        self.controlWidget=ControlWidget()

        #self.ns = {'app': self,'os':os,'sys':sys,'pg':pg,'np':np,'help':self.help,'rpc':self.rpc}
        self.ns = {'app': self,'os':os,'sys':sys,'pg':pg,'np':np}
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"FFT Tab")
        self.tabs.addTab(self.tab2,"Calib Tab")
        
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.pushButton1 = QPushButton("Set input")
        self.tab1.layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1.layout)

        # Create second tab        
        self.col = QColor(0, 0, 0)

        self.tab2.layout = QVBoxLayout(self)
        self.linear = QtGui.QPushButton("Linearization")
        self.linear.setCheckable(True)
        #self.linear.move(10, 10)
        self.linear.clicked[bool].connect(self.setGraph)
        self.tab2.layout.addWidget(self.linear,0,0)
        self.tab2.setLayout(self.tab2.layout)  

        self.flat = QPushButton("Cumsum flattening")
        self.flat.setCheckable(True)
        #self.flat.move(10, 60)
        self.flat.clicked[bool].connect(self.setGraph)
        self.tab2.layout.addWidget(self.flat,0,1)
        self.tab2.setLayout(self.tab2.layout)  

        self.calib = QPushButton("Chip calib")
        self.calib.setCheckable(True)
        self.calib.move(10, 110)
        self.calib.clicked[bool].connect(self.setGraph)
        self.tab2.layout.addWidget(self.calib,0,2)
        self.tab2.setLayout(self.tab2.layout) 

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
            self.col.name())

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Starta GUI')
        self.show()

        # Create labels & textboxes
        self.label = QLabel('linearization: # iterations',1,0)
        self.label.move(200,40)
        self.tab2.layout.addWidget(self.label)
        self.tab2.setLayout(self.tab2.layout)

        # layout.addWidget(QtGui.QLabel("linearization: # iterations"),1,0)
        # layout.addWidget(self.ctrl_ver,1,1)
        # layout.addWidget(QtGui.QLineEdit(self,1,2)
        # layout.addWidget(QtGui.QLabel("flattening: Vstart, Kp, Ki, Kd"),1,3)
        # layout.addWidget(self.ctrl_ver,1,4)
        # layout.addWidget(QtGui.QLineEdit(self,1,5)
        # layout.addWidget(QtGui.QLabel("Chip calib: amp_attenuation"),1,6)
        # layout.addWidget(self.ctrl_ver,1,7)
        # layout.addWidget(QtGui.QLineEdit(self,1,8)

        self.calib = QPushButton("Set input")
        self.tab2.layout.addWidget(self.calib,1,9)
        self.tab2.setLayout(self.tab2.layout) 

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
    
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
   
    def closeAll(self):
        
        self.tele_tab.close_all()    
            
    

def start(args):
    
    app=    QtGui.QApplication([])
    app.setStyle('Windows')
    gui = App(app)
    app.instance().exec_() 
  
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

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = App()
#     sys.exit(app.exec_())

if __name__ == '__main__':
    start(None) 