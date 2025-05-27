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

from fbs_runtime.application_context import ApplicationContext
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import sys

class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

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

    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Group 1")

        togglePushButton = QPushButton("Linearization")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        togglePushButton = QPushButton("Cumsum flattening")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        togglePushButton = QPushButton("Chip calib")
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(togglePushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(togglePushButton)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

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
    appctxt = ApplicationContext()
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(appctxt.app.exec_())