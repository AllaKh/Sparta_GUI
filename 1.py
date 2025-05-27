import sys,os

import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot

class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 300
        self.height = 200
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.createGridLayout()
        
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        
        self.show()
    
    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        layout.setColumnStretch(1, 4)
        layout.setColumnStretch(2, 4)
        
        layout.addWidget(QPushButton('Linearization'),0,0)
        layout.addWidget(QPushButton('Cumsum flattening'),1,0)
        layout.addWidget(QPushButton('Chip calib'),2,0)

        layout.addWidget(QPushButton('7'),0,2)
        layout.addWidget(QPushButton('8'),1,2)
        layout.addWidget(QPushButton('9'),2,2)
        
        # # Create second tab        
        # self.linear = layout.addWidget(QPushButton('Linearization'),0,0)
        # self.linear.setCheckable(True)
        # self.linear.move(10, 10)
        # self.linear.clicked[bool].connect(self.setGraph)
        # #self.tab2.layout.addWidget(self.linear)
        # self.tab2.setLayout(self.tab2.layout)       

        # self.flat = layout.addWidget(QPushButton('Cumsum flattening'),0,1)
        # self.flat.setCheckable(True)
        # self.flat.move(10, 60)
        # self.flat.clicked[bool].connect(self.setGraph)
        # #self.tab2.layout.addWidget(self.flat)
        # #self.tab2.setLayout(self.tab2.layout)  

        # self.calib = layout.addWidget(QPushButton('Chip calib'),0,2)
        # self.calib.setCheckable(True)
        # self.calib.move(10, 110)
        # self.calib.clicked[bool].connect(self.setGraph)
        # #self.tab2.layout.addWidget(self.calib)
        # #self.tab2.setLayout(self.tab2.layout) 

        # self.square = QFrame(self)
        # self.square.setGeometry(150, 20, 100, 100)
        # self.square.setStyleSheet("QWidget { background-color: %s }" %
        #     self.col.name())

        # self.setGeometry(300, 300, 300, 200)
        # self.setWindowTitle('Starta GUI')
        # self.show()

        # Create labels & textboxes
        layout.addWidget(QLabel('linearization: # iterations'),0,1)
        #self.label.move(200,40)
        #self.tab2.layout.addWidget(self.label)
        #self.tab2.setLayout(self.tab2.layout)

        layout.addWidget(QLineEdit(self),1,1)
        #self.textbox1.move(200, 60)
        #self.tab2.layout.addWidget(self.textbox1)
        #self.tab2.setLayout(self.tab2.layout)

        layout.addWidget(QLabel('flattening: Vstart, Kp, Ki, Kd'),2,1)
        #self.labe2.move(200,90)
        #self.tab2.layout.addWidget(self.labe2)
        #self.tab2.setLayout(self.tab2.layout)

        layout.addWidget(QLineEdit(self),3,1)
        #self.textbox2.move(200, 110)
        #self.textbox2.resize(280,40)
        # self.tab2.layout.addWidget(self.textbox2)
        # self.tab2.setLayout(self.tab2.layout)

        layout.addWidget(QLabel('Chip calib: amp_attenuation'),4,1)
        #self.labe3.move(200,130)
        #self.tab2.layout.addWidget(self.labe3)
        #self.tab2.setLayout(self.tab2.layout)

        layout.addWidget(QLineEdit(self),5,1)
        #self.textbox3.move(200, 140)
        #self.textbox3.resize(280,40)
        # self.tab2.layout.addWidget(self.textbox3)
        # self.tab2.setLayout(self.tab2.layout)

        layout.addWidget(QPushButton("Set input"),6,1)
        #self.setinput2.setCheckable(True)
        # self.setinput2.move(200, 200)
        # self.tab2.layout.addWidget(self.setinput2)
        # self.tab2.setLayout(self.tab2.layout)

        # Add tabs to widget
        #self.layout.addWidget(self.tabs)
        #self.setLayout(self.layout)

        self.horizontalGroupBox.setLayout(layout) 
  
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