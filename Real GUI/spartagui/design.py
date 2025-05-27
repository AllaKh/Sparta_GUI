# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot,pyqtProperty,QObject,QFile
import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.console
from pyqtgraph.parametertree import Parameter, ParameterTree

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1127, 909)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Initialize tab screen
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1131, 871))
        self.tabWidget.setObjectName("tabWidget")

        # Create first tab
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        #Camera
        # self.graphicsView_5 = QtWidgets.QGraphicsView(self.tab)
        # self.graphicsView_5.setGeometry(QtCore.QRect(10, 20, 401, 361))
        # self.graphicsView_5.setObjectName("graphicsView_5")
        self.graphicsView_5 = PlotCanvas(self.tab, width=4.5, height=4)
        self.graphicsView_5.move(0,0)

        #Cursor position
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(20, 410, 81, 21))
        self.label_4.setObjectName("label_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_4.setGeometry(QtCore.QRect(100, 410, 141, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")

        #Set Input Cursor position
        self.pushButton_5 = QtWidgets.QPushButton(self.tab)
        self.pushButton_5.setGeometry(QtCore.QRect(290, 400, 111, 41))
        self.pushButton_5.setObjectName("pushButton_5")

        #Time domain
        # self.graphicsView_6 = QtWidgets.QGraphicsView(self.tab)
        # self.graphicsView_6.setGeometry(QtCore.QRect(10, 460, 401, 381))
        # self.graphicsView_6.setObjectName("graphicsView_6")    
        self.graphicsView_6 = PlotCanvas(self.tab, width=4.5, height=4)
        self.graphicsView_6.move(0,450)

        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setGeometry(QtCore.QRect(420, 20, 20, 821))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        #X lims
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(490, 20, 41, 31))
        self.label_6.setObjectName("label_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_7.setGeometry(QtCore.QRect(440, 50, 141, 31))
        self.lineEdit_7.setObjectName("lineEdit_7")

        #Y lims
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(490, 90, 41, 31))
        self.label_7.setObjectName("label_7")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_5.setGeometry(QtCore.QRect(440, 120, 141, 31))
        self.lineEdit_5.setObjectName("lineEdit_5")

        #N chirps
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(490, 170, 47, 14))
        self.label_5.setObjectName("label_5")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_6.setGeometry(QtCore.QRect(440, 190, 141, 31))
        self.lineEdit_6.setObjectName("lineEdit_6")

        self.line_3 = QtWidgets.QFrame(self.tab)
        self.line_3.setGeometry(QtCore.QRect(430, 240, 161, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        # Analisis
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(490, 270, 47, 14))
        self.label_8.setObjectName("label_8")
        self.radioButton = QtWidgets.QRadioButton(self.tab)
        self.radioButton.setGeometry(QtCore.QRect(450, 300, 74, 18))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_2.setGeometry(QtCore.QRect(450, 320, 74, 18))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_3.setGeometry(QtCore.QRect(450, 340, 74, 18))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(self.tab)
        self.radioButton_4.setGeometry(QtCore.QRect(450, 360, 74, 18))
        self.radioButton_4.setObjectName("radioButton_4")

        self.line_4 = QtWidgets.QFrame(self.tab)
        self.line_4.setGeometry(QtCore.QRect(430, 390, 161, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")

        #SNR
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(490, 420, 47, 14))
        self.label_9.setObjectName("label_9")

        #Noise bin range
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(470, 450, 81, 16))
        self.label_10.setObjectName("label_10")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_8.setGeometry(QtCore.QRect(440, 470, 141, 31))
        self.lineEdit_8.setObjectName("lineEdit_8")

        #Signal bin range
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(470, 520, 91, 16))
        self.label_11.setObjectName("label_11")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_9.setGeometry(QtCore.QRect(440, 550, 141, 31))
        self.lineEdit_9.setObjectName("lineEdit_9")

        self.line_5 = QtWidgets.QFrame(self.tab)
        self.line_5.setGeometry(QtCore.QRect(430, 610, 161, 16))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.tab)
        self.line_6.setGeometry(QtCore.QRect(583, 20, 20, 821))
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")

        #Set Input
        self.pushButton_6 = QtWidgets.QPushButton(self.tab)
        self.pushButton_6.setGeometry(QtCore.QRect(444, 680, 131, 61))
        self.pushButton_6.setObjectName("pushButton_6")

        #Main FFT display
        self.graphicsView_7 = QtWidgets.QGraphicsView(self.tab)
        self.graphicsView_7.setGeometry(QtCore.QRect(600, 10, 511, 701))
        self.graphicsView_7.setObjectName("graphicsView_7")

        #Save
        self.lineEdit_10 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_10.setGeometry(QtCore.QRect(600, 750, 281, 51))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.toolButton = QtWidgets.QToolButton(self.tab)
        self.toolButton.setGeometry(QtCore.QRect(890, 760, 51, 31))
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.browse_folder)
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(960, 742, 141, 61))
        self.pushButton_7.setObjectName("pushButton_7")

        self.tabWidget.addTab(self.tab, "")

        # Create second tab 
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        #Linearization button
        self.pushButton = QtWidgets.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(40, 120, 111, 61))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton.toggled.connect(self.linear)

        #Cumsum flattening button
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 250, 111, 61))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.toggled.connect(self.flat)        

        #Chip calib button
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 390, 111, 61))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.toggled.connect(self.calib)          

        #linearization: # iterations
        self.label = QtWidgets.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(250, 60, 191, 51))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit.setGeometry(QtCore.QRect(250, 110, 171, 31))
        self.lineEdit.setObjectName("lineEdit")

        #flattening: Vstart, Kp, Ki, Kd
        self.label_2 = QtWidgets.QLabel(self.tab_2)
        self.label_2.setGeometry(QtCore.QRect(250, 200, 191, 51))
        self.label_2.setObjectName("label_2")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(250, 250, 171, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")

        #Chip calib: amp_attenuation
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(250, 370, 191, 51))
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(250, 420, 171, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")        

        # Set Calib Input button
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(260, 540, 151, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.setInput)

        self.line = QtWidgets.QFrame(self.tab_2)
        self.line.setGeometry(QtCore.QRect(190, 40, 20, 691))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #VCO display 
        self.graphicsView = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView.setGeometry(QtCore.QRect(490, 60, 256, 192))
        self.graphicsView.setObjectName("graphicsView")

        #MCT
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView_2.setGeometry(QtCore.QRect(810, 60, 256, 192))
        self.graphicsView_2.setObjectName("graphicsView_2")

        #Cumsum error
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView_3.setGeometry(QtCore.QRect(490, 450, 256, 192))
        self.graphicsView_3.setObjectName("graphicsView_3")

        #1bit average 
        self.graphicsView_4 = QtWidgets.QGraphicsView(self.tab_2)
        self.graphicsView_4.setGeometry(QtCore.QRect(820, 450, 256, 192))
        self.graphicsView_4.setObjectName("graphicsView_4")

        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1127, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sparta GUI"))
        self.label_4.setText(_translate("MainWindow", "Cursor position"))
        self.pushButton_5.setText(_translate("MainWindow", "Set Camera Input"))
        self.label_6.setText(_translate("MainWindow", "X lims"))
        self.label_7.setText(_translate("MainWindow", "Y lims"))
        self.label_5.setText(_translate("MainWindow", "N chirps"))
        self.label_8.setText(_translate("MainWindow", "Analysis:"))
        self.radioButton.setText(_translate("MainWindow", "mean"))
        self.radioButton_2.setText(_translate("MainWindow", "STD"))
        self.radioButton_3.setText(_translate("MainWindow", "max"))
        self.radioButton_4.setText(_translate("MainWindow", "min"))
        self.label_9.setText(_translate("MainWindow", "SNR"))
        self.label_10.setText(_translate("MainWindow", "Noise bin range"))
        self.label_11.setText(_translate("MainWindow", "Signal bin range"))
        self.pushButton_6.setText(_translate("MainWindow", "Set FFT Input"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.pushButton_7.setText(_translate("MainWindow", "Save data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "FFT Tab"))
        self.pushButton.setText(_translate("MainWindow", "Linearization"))
        self.pushButton_2.setText(_translate("MainWindow", "Cumsum flattening"))
        self.pushButton_3.setText(_translate("MainWindow", "Chip calib"))
        self.label.setText(_translate("MainWindow", "linearization: # iterations"))
        self.label_2.setText(_translate("MainWindow", "flattening: Vstart, Kp, Ki, Kd"))
        self.label_3.setText(_translate("MainWindow", "Chip calib: amp_attenuation"))
        self.pushButton_4.setText(_translate("MainWindow", "Set Calib Input"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Calib Tab"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def browse_folder(self):
        #self.tabWidget.clear()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose folder")

        if directory:
            for file_name in os.listdir(directory):
                self.tabWidget.addItem(file_name)

    def setInput(self):
        if not self.lineEdit.text() or not self.lineEdit_2.text() or not self.lineEdit_3.text():
            print("Please enter all three values")
        else:
            print(self.lineEdit.text() + self.lineEdit_2.text() + self.lineEdit_3.text())  

    @QtCore.pyqtSlot(bool)
    def linear(self,checked):
        if checked:
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.rowOverride = True
        elif not checked:
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.rowOverride = False

    def flat(self,checked):
        if checked:
            self.pushButton.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.rowOverride = True
        elif not checked:
            self.pushButton.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.rowOverride = False

    def calib(self,checked):
        if checked:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.rowOverride = True
        elif not checked:
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.rowOverride = False            

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=4.5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    #filename="C:\Orix_SDK\workDir\sr_pfe_dump_quarter_0.csv"
    #file = open(filename, "r")
    #reader = csv.reader(file)

    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('Camera')
        self.draw()              