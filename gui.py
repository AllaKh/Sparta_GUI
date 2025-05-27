# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys,os

import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

from PyQt5.QtWidgets import (QWidget, QPushButton,
    QFrame, QMainWindow, QAction, qApp, QApplication)
from PyQt5.QtGui import QColor,QIcon

class Tab(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        fftAction = QAction(QIcon('exit.png'), '&FFT Tab', self)
        fftAction.setShortcut('Ctrl+1')
        fftAction.setStatusTip('Switch to FFT Tab')
        fftAction.triggered.connect(qApp.quit)
        
        calibAction = QAction(QIcon('exit.png'), '&Calib Tab', self)
        calibAction.setShortcut('Ctrl+2')
        calibAction.setStatusTip('Switch to Calib Tab')
        calibAction.triggered.connect(qApp.quit)        
        
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

     
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&FFT Tab')
        fileMenu.addAction(exitAction)
        
        menubar1 = self.menuBar()
        fileMenu = menubar.addMenu('&Calib Tab')
        fileMenu.addAction(exitAction)        

        menubar2 = self.menuBar()
        fileMenu = menubar.addMenu('&Exit')
        fileMenu.addAction(exitAction)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Starta GUI')
        self.show()

class Buttons(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.col = QColor(0, 0, 0)

        redb = QPushButton('Linearization', self)
        redb.setCheckable(True)
        redb.move(10, 10)

        redb.clicked[bool].connect(self.setGraph)

        greenb = QPushButton('Cumsum flattening', self)
        greenb.setCheckable(True)
        greenb.move(10, 60)

        greenb.clicked[bool].connect(self.setGraph)

        blueb = QPushButton('Chip calib', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setGraph)

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %
            self.col.name())

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Toggle button')
        self.show()


    def setGraph(self, pressed):

        source = self.sender()

        if pressed:
            val = 255
        else: val = 0

        if source.text() == "Linearization":
            self.col.setRed(val)
        elif source.text() == "Cumsum flattening":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)

        self.square.setStyleSheet("QFrame { background-color: %s }" %
            self.col.name())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Tab(),Buttons()     
#    ex1 = Buttons()
    sys.exit(app.exec_())