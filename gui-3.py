import sys,os

import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Sparta GUI'
        # self.left = 0
        # self.top = 0
        # self.width = 300
        # self.height = 200
        self.setWindowTitle(self.title)
        # self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)
        
        self.show()
    
class MyTableWidget(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
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
        self.linear = QPushButton("Linearization")
        self.linear.setCheckable(True)
        self.linear.move(10, 10)
        self.linear.clicked[bool].connect(self.setGraph)
        self.tab2.layout.addWidget(self.linear)
        self.tab2.setLayout(self.tab2.layout)       

        self.flat = QPushButton("Cumsum flattening")
        self.flat.setCheckable(True)
        self.flat.move(10, 60)
        self.flat.clicked[bool].connect(self.setGraph)
        self.tab2.layout.addWidget(self.flat)
        self.tab2.setLayout(self.tab2.layout)  

        self.calib = QPushButton("Chip calib")
        self.calib.setCheckable(True)
        self.calib.move(10, 110)
        self.calib.clicked[bool].connect(self.setGraph)
        self.tab2.layout.addWidget(self.calib)
        self.tab2.setLayout(self.tab2.layout) 

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
            self.col.name())

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Starta GUI')
        self.show()

        # Create labels & textboxes
        self.label = QLabel('linearization: # iterations')
        self.label.move(200,40)
        self.tab2.layout.addWidget(self.label)
        self.tab2.setLayout(self.tab2.layout)

        self.textbox1 = QLineEdit(self)
        self.textbox1.move(200, 60)
        #self.textbox1.resize(280,40)
        self.tab2.layout.addWidget(self.textbox1)
        self.tab2.setLayout(self.tab2.layout)

        self.labe2 = QLabel('flattening: Vstart, Kp, Ki, Kd')
        self.labe2.move(200,90)
        self.tab2.layout.addWidget(self.labe2)
        self.tab2.setLayout(self.tab2.layout)

        self.textbox2 = QLineEdit(self)
        self.textbox2.move(200, 110)
        #self.textbox2.resize(280,40)
        self.tab2.layout.addWidget(self.textbox2)
        self.tab2.setLayout(self.tab2.layout)

        self.labe3 = QLabel('Chip calib: amp_attenuation')
        self.labe3.move(200,130)
        self.tab2.layout.addWidget(self.labe3)
        self.tab2.setLayout(self.tab2.layout)

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(200, 140)
        #self.textbox3.resize(280,40)
        self.tab2.layout.addWidget(self.textbox3)
        self.tab2.setLayout(self.tab2.layout)

        self.setinput2 = QPushButton("Set input")
        #self.setinput2.setCheckable(True)
        self.setinput2.move(200, 200)
        self.tab2.layout.addWidget(self.setinput2)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())