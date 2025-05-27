# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
#from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import *
#from qline import Ui_MainWindow
import numpy as np
import datetime,time

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import pyqtgraph as pg

import csv
import random
from ximea import xiapi
import cv2
import sys

import queue_data_classes

class Ui_MainWindow(object):
    def __init__(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        # noinspection PyArgumentList
        self.timer.start(1)
    
    def setupUi(self, MainWindow):
        self.Mainwin=MainWindow
        self.Mainwin.setObjectName("MainWindow")
        self.Mainwin.resize(1127, 909)
        self.centralwidget = QtWidgets.QWidget(self.Mainwin)
        self.centralwidget.setObjectName("centralwidget")     

        # Initialize tab screen
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1131, 871))
        self.tabWidget.setObjectName("tabWidget")

        # Create first tab
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")

        #Camera
        self.graphicsView_Camera = QtWidgets.QGraphicsView(self.tab)
        self.graphicsView_Camera.setGeometry(QtCore.QRect(10, 20, 401, 361))
        self.graphicsView_Camera.setObjectName("graphicsView_5")
        # self.graphicsView_Camera = Camera(self.tab, width=4.5, height=4)
        # self.graphicsView_Camera.move(0,0)

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
        self.graphicsView_TD = TimeDomain(self.tab, width=4.5, height=4)
        self.graphicsView_TD.move(0,450)
        #self.model.dataChanged.connect(self.finishedEdit)

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
        # self.graphicsView_7 = QtWidgets.QGraphicsView(self.tab)
        # self.graphicsView_7.setGeometry(QtCore.QRect(600, 10, 511, 701))
        # self.graphicsView_7.setObjectName("graphicsView_7")
        self.graphicsView_FFT = FFTDisp(self.tab, width=5.5, height=8.5)
        self.graphicsView_FFT.move(595,-50)
        
        #Save
        self.lineEdit_10 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_10.setGeometry(QtCore.QRect(600, 750, 281, 51))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.toolButton = QtWidgets.QToolButton(self.tab)
        self.toolButton.setGeometry(QtCore.QRect(890, 760, 51, 31))
        self.toolButton.setObjectName("toolButton")
        #self.toolButton.clicked.connect(self.browse_folder)
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

        #Scope IP and naive connect
        self.label_scope_IP = QtWidgets.QLabel(self.tab_2)
        self.label_scope_IP.setGeometry(QtCore.QRect(220, 10, 61, 16))
        self.label_scope_IP.setObjectName("label_scope_IP")
        self.scope_IP = QtWidgets.QLineEdit(self.tab_2)
        self.scope_IP.setGeometry(QtCore.QRect(350, 10, 113, 20))
        self.scope_IP.setObjectName("scope_IP")
        self.scope_IP.setText(self.Mainwin.calib_dat.scope_IP)

        self.label_naive_connect = QtWidgets.QLabel(self.tab_2)
        self.label_naive_connect.setGeometry(QtCore.QRect(220, 40, 81, 16))
        self.label_naive_connect.setObjectName("label_naive_connect")
        self.naive_connect = QtWidgets.QLineEdit(self.tab_2)
        self.naive_connect.setGeometry(QtCore.QRect(350, 40, 113, 20))
        self.naive_connect.setObjectName("naive_connect")
        self.naive_connect.setText(str(self.Mainwin.calib_dat.naive_connect))

        #linearization: # iterations
        self.label_lin_dat = QtWidgets.QLabel(self.tab_2)
        self.label_lin_dat.setGeometry(QtCore.QRect(310, 90, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_lin_dat.setFont(font)
        self.label_lin_dat.setObjectName("label_lin_dat")   

        #number of iterations/vector
        self.label_iters = QtWidgets.QLabel(self.tab_2)
        self.label_iters.setGeometry(QtCore.QRect(220, 130, 111, 16))
        self.label_iters.setObjectName("label_iters")
        self.iters = QtWidgets.QLineEdit(self.tab_2)
        self.iters.setGeometry(QtCore.QRect(350, 130, 113, 20))
        self.iters.setObjectName("iters")
        self.iters.setText(str(self.Mainwin.calib_dat.lin_dat.iters))

        #slices to ignore []
        self.label_slice_ignore = QtWidgets.QLabel(self.tab_2)
        self.label_slice_ignore.setGeometry(QtCore.QRect(220, 160, 81, 16))
        self.label_slice_ignore.setObjectName("label_slice_ignore")
        self.slice_ignore = QtWidgets.QLineEdit(self.tab_2)
        self.slice_ignore.setGeometry(QtCore.QRect(350, 160, 113, 20))
        self.slice_ignore.setObjectName("slice_ignore")
        self.slice_ignore.setText(str(self.Mainwin.calib_dat.lin_dat.slice_ignore))

        #number of sub pulses
        self.label_sub_pulse_times = QtWidgets.QLabel(self.tab_2)
        self.label_sub_pulse_times.setGeometry(QtCore.QRect(220, 190, 71, 16))
        self.label_sub_pulse_times.setObjectName("label_sub_pulse_times")
        self.sub_pulse_times = QtWidgets.QLineEdit(self.tab_2)
        self.sub_pulse_times.setGeometry(QtCore.QRect(350, 190, 113, 20))
        self.sub_pulse_times.setObjectName("sub_pulse_times")
        self.sub_pulse_times.setText(str(self.Mainwin.calib_dat.lin_dat.sub_pulse_times))

        #target center frequency
        self.label_target_freq = QtWidgets.QLabel(self.tab_2)
        self.label_target_freq.setGeometry(QtCore.QRect(220, 220, 91, 16))
        self.label_target_freq.setObjectName("label_target_freq")
        self.target_freq = QtWidgets.QLineEdit(self.tab_2)
        self.target_freq.setGeometry(QtCore.QRect(350, 220, 113, 20))
        self.target_freq.setObjectName("target_freq")
        self.target_freq.setText("{:.2e}".format(self.Mainwin.calib_dat.lin_dat.target_freq))

        #set scope time and time delay
        self.label_set_scope = QtWidgets.QLabel(self.tab_2)
        self.label_set_scope.setGeometry(QtCore.QRect(220, 250, 61, 20))
        self.label_set_scope.setObjectName("label_set_scope")
        self.label_scope_scale = QtWidgets.QLabel(self.tab_2)
        self.label_scope_scale.setGeometry(QtCore.QRect(280, 250, 31, 16))
        self.label_scope_scale.setObjectName("label_scope_scale")
        self.scope_scale = QtWidgets.QLineEdit(self.tab_2)
        self.scope_scale.setGeometry(QtCore.QRect(310, 250, 51, 20))
        self.scope_scale.setObjectName("scope_scale")
        self.scope_scale.setText("{:.2e}".format(self.Mainwin.calib_dat.lin_dat.scope_scale))

        self.label_scope_delay = QtWidgets.QLabel(self.tab_2)
        self.label_scope_delay.setGeometry(QtCore.QRect(380, 250, 31, 16))
        self.label_scope_delay.setObjectName("label_scope_delay")
        self.scope_delay = QtWidgets.QLineEdit(self.tab_2)
        self.scope_delay.setGeometry(QtCore.QRect(410, 250, 51, 20))
        self.scope_delay.setObjectName("scope_delay")
        self.scope_delay.setText("{:.2e}".format(self.Mainwin.calib_dat.lin_dat.scope_delay))

        #lin file name
        self.label_lin_file_name = QtWidgets.QLabel(self.tab_2)
        self.label_lin_file_name.setGeometry(QtCore.QRect(220, 280, 47, 14))
        self.label_lin_file_name.setObjectName("label_lin_file_name")
        self.lin_file_name = QtWidgets.QLineEdit(self.tab_2)
        self.lin_file_name.setGeometry(QtCore.QRect(280, 280, 113, 20))
        self.lin_file_name.setObjectName("lin_file_name")
        self.lin_file_name.setText(self.Mainwin.calib_dat.lin_dat.file_name)

        self.toolButton_linear = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_linear.setGeometry(QtCore.QRect(420, 280, 23, 20))
        self.toolButton_linear.setObjectName("toolButton_linear")
        self.toolButton_linear.clicked.connect(self.lin_getfiles)

        #Flattening
        self.label_cums_dat = QtWidgets.QLabel(self.tab_2)
        self.label_cums_dat.setGeometry(QtCore.QRect(320, 350, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_cums_dat.setFont(font)
        self.label_cums_dat.setObjectName("label_cums_dat")

        #CMPIN_SEL (calibration mode: D2S or GM_DAC)
        self.label_by_D2S = QtWidgets.QLabel(self.tab_2)
        self.label_by_D2S.setGeometry(QtCore.QRect(220, 390, 71, 16))
        self.label_by_D2S.setObjectName("label_by_D2S")
        self.by_D2S = QtWidgets.QLineEdit(self.tab_2)
        self.by_D2S.setGeometry(QtCore.QRect(350, 390, 113, 20))
        self.by_D2S.setObjectName("by_D2S")
        self.by_D2S.setText(str(self.Mainwin.calib_dat.cums_dat.by_D2S))

        #V0 
        self.label_V0 = QtWidgets.QLabel(self.tab_2)
        self.label_V0.setGeometry(QtCore.QRect(220, 420, 21, 16))
        self.label_V0.setObjectName("label_V0")
        self.V0 = QtWidgets.QLineEdit(self.tab_2)
        self.V0.setGeometry(QtCore.QRect(250, 420, 61, 20))
        self.V0.setObjectName("V0")
        self.V0.setText(str(self.Mainwin.calib_dat.cums_dat.V0))

        #Kd
        self.label_Kd = QtWidgets.QLabel(self.tab_2)
        self.label_Kd.setGeometry(QtCore.QRect(370, 420, 21, 16))
        self.label_Kd.setObjectName("label_Kd")
        self.Kd = QtWidgets.QLineEdit(self.tab_2)
        self.Kd.setGeometry(QtCore.QRect(400, 420, 61, 20))
        self.Kd.setObjectName("Kd")
        self.Kd.setText(str(self.Mainwin.calib_dat.cums_dat.Kd))

        #Kp
        self.label_Kp = QtWidgets.QLabel(self.tab_2)
        self.label_Kp.setGeometry(QtCore.QRect(220, 450, 21, 16))
        self.label_Kp.setObjectName("label_Kp")
        self.Kp = QtWidgets.QLineEdit(self.tab_2)
        self.Kp.setGeometry(QtCore.QRect(250, 450, 61, 20))
        self.Kp.setObjectName("Kp")
        self.Kp.setText("{:.2e}".format(self.Mainwin.calib_dat.cums_dat.Kp))

        #Ki
        self.label_Ki = QtWidgets.QLabel(self.tab_2)
        self.label_Ki.setGeometry(QtCore.QRect(370, 450, 21, 16))
        self.label_Ki.setObjectName("label_Ki")
        self.Ki = QtWidgets.QLineEdit(self.tab_2)
        self.Ki.setGeometry(QtCore.QRect(400, 450, 61, 20))
        self.Ki.setObjectName("Ki")
        self.Ki.setText(str(self.Mainwin.calib_dat.cums_dat.Ki))
        
        #flat file
        self.label_flat_file_name = QtWidgets.QLabel(self.tab_2)
        self.label_flat_file_name.setGeometry(QtCore.QRect(220, 480, 41, 16))
        self.label_flat_file_name.setObjectName("label_flat_file_name")
        self.flat_file_name = QtWidgets.QLineEdit(self.tab_2)
        self.flat_file_name.setGeometry(QtCore.QRect(280, 480, 113, 20))
        self.flat_file_name.setObjectName("flat_file_name")
        self.flat_file_name.setText(self.Mainwin.calib_dat.cums_dat.file_name)

        self.toolButton_flat = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_flat.setGeometry(QtCore.QRect(420, 480, 23, 20))
        self.toolButton_flat.setObjectName("toolButton_flat")
        self.toolButton_flat.clicked.connect(self.flat_getfiles)

        #Chip calibration
        self.label_chip_dat = QtWidgets.QLabel(self.tab_2)
        self.label_chip_dat.setGeometry(QtCore.QRect(310, 550, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_chip_dat.setFont(font)
        self.label_chip_dat.setObjectName("label_chip_dat")

        #Vbias
        self.label_Vbias = QtWidgets.QLabel(self.tab_2)
        self.label_Vbias.setGeometry(QtCore.QRect(220, 590, 31, 16))
        self.label_Vbias.setObjectName("label_Vbias")
        self.Vbias = QtWidgets.QLineEdit(self.tab_2)
        self.Vbias.setGeometry(QtCore.QRect(350, 590, 113, 20))
        self.Vbias.setObjectName("Vbias")
        self.Vbias.setText("{:.2e}".format(self.Mainwin.calib_dat.chip_dat.Vbias))       

        #GM_DAC
        self.label_GM_DAC = QtWidgets.QLabel(self.tab_2)
        self.label_GM_DAC.setGeometry(QtCore.QRect(220, 620, 51, 16))
        self.label_GM_DAC.setObjectName("label_GM_DAC")
        self.GM_DAC = QtWidgets.QLineEdit(self.tab_2)
        self.GM_DAC.setGeometry(QtCore.QRect(350, 620, 113, 20))
        self.GM_DAC.setObjectName("GM_DAC")
        self.GM_DAC.setText(str(self.Mainwin.calib_dat.chip_dat.GM_DAC)) 

        #AMP_ATT
        self.label_AMP_ATT = QtWidgets.QLabel(self.tab_2)
        self.label_AMP_ATT.setGeometry(QtCore.QRect(220, 650, 61, 16))
        self.label_AMP_ATT.setObjectName("label_AMP_ATT")
        self.AMP_ATT = QtWidgets.QLineEdit(self.tab_2)
        self.AMP_ATT.setGeometry(QtCore.QRect(350, 650, 113, 20))
        self.AMP_ATT.setObjectName("AMP_ATT")
        self.AMP_ATT.setText(str(self.Mainwin.calib_dat.chip_dat.AMP_ATT)) 

        #Set scope
        self.label_set_scope_2 = QtWidgets.QLabel(self.tab_2)
        self.label_set_scope_2.setGeometry(QtCore.QRect(220, 680, 61, 20))
        self.label_set_scope_2.setObjectName("label_set_scope_2")
        self.label_scope_scale_2 = QtWidgets.QLabel(self.tab_2)
        self.label_scope_scale_2.setGeometry(QtCore.QRect(290, 680, 31, 16))
        self.label_scope_scale_2.setObjectName("label_scope_scale_2")
        self.scope_scale_2 = QtWidgets.QLineEdit(self.tab_2)
        self.scope_scale_2.setGeometry(QtCore.QRect(320, 680, 51, 20))
        self.scope_scale_2.setObjectName("scope_scale_2")
        self.scope_scale_2.setText("{:.2e}".format(self.Mainwin.calib_dat.chip_dat.scope_scale))  

        self.label_scope_delay_2 = QtWidgets.QLabel(self.tab_2)
        self.label_scope_delay_2.setGeometry(QtCore.QRect(380, 680, 31, 16))
        self.label_scope_delay_2.setObjectName("label_scope_delay_2")
        self.scope_delay_2 = QtWidgets.QLineEdit(self.tab_2)
        self.scope_delay_2.setGeometry(QtCore.QRect(410, 680, 51, 20))
        self.scope_delay_2.setObjectName("scope_delay_2")
        self.scope_delay_2.setText("{:.2e}".format(self.Mainwin.calib_dat.chip_dat.scope_delay)) 

        #calib file
        self.label_calib_file_name = QtWidgets.QLabel(self.tab_2)
        self.label_calib_file_name.setGeometry(QtCore.QRect(220, 710, 47, 14))
        self.label_calib_file_name.setObjectName("label_calib_file_name")
        self.calib_file_name = QtWidgets.QLineEdit(self.tab_2)
        self.calib_file_name.setGeometry(QtCore.QRect(290, 710, 113, 20))
        self.calib_file_name.setObjectName("calib_file_name")
        self.calib_file_name.setText(self.Mainwin.calib_dat.chip_dat.file_name)

        self.toolButton_calib = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_calib.setGeometry(QtCore.QRect(430, 710, 23, 20))
        self.toolButton_calib.setObjectName("toolButton_calib")
        self.toolButton_calib.clicked.connect(self.calib_getfiles)

        # Set Calib Input button
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(250, 770, 151, 61))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.setInput)

        self.line = QtWidgets.QFrame(self.tab_2)
        self.line.setGeometry(QtCore.QRect(190, 40, 20, 811))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #VCO display 
        # self.graphicsView = QtWidgets.QGraphicsView(self.tab_2)
        # self.graphicsView.setGeometry(QtCore.QRect(490, 60, 256, 192))
        # self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_VCO = VCO(self.tab_2, width=3.5, height=3.5)
        self.graphicsView_VCO.move(470,0)        

        #Linearization 
        # self.graphicsView_2 = QtWidgets.QGraphicsView(self.tab_2)
        # self.graphicsView_2.setGeometry(QtCore.QRect(840, 60, 256, 192))
        # self.graphicsView_2.setObjectName("graphicsView_2")
        self.graphicsView_Lin = Linearization(self.tab_2, width=3.5, height=3.5)
        self.graphicsView_Lin.move(790,0)            

        #Cumsum error
        # self.graphicsView_3 = QtWidgets.QGraphicsView(self.tab_2)
        # self.graphicsView_3.setGeometry(QtCore.QRect(490, 450, 256, 192))
        # self.graphicsView_3.setObjectName("graphicsView_3")
        self.graphicsView_Cumsum = CumsumError(self.tab_2, width=3.5, height=3.5)
        self.graphicsView_Cumsum.move(470,400) 

        #1bit average 
        # self.graphicsView_4 = QtWidgets.QGraphicsView(self.tab_2)
        # self.graphicsView_4.setGeometry(QtCore.QRect(850, 450, 256, 192))
        # self.graphicsView_4.setObjectName("graphicsView_4")
        self.graphicsView_1bit = OneBit(self.tab_2, width=3.5, height=3.5)
        self.graphicsView_1bit.move(790,400) 

        self.tabWidget.addTab(self.tab_2, "")
        self.Mainwin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.Mainwin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1127, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.Mainwin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.Mainwin)
        self.statusbar.setObjectName("statusbar")
        self.Mainwin.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(self.Mainwin)
        self.actionOpen.setObjectName("actionOpen")
        self.actionSave = QtWidgets.QAction(self.Mainwin)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_as = QtWidgets.QAction(self.Mainwin)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionExit = QtWidgets.QAction(self.Mainwin)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addAction(self.actionExit)
        self.actionExit.triggered.connect(self.close)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(self.Mainwin)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self.Mainwin)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.Mainwin.setWindowTitle(_translate("MainWindow", "Sparta GUI"))
        self.label_4.setText(_translate("MainWindow", "Cursor position"))
        self.pushButton_5.setText(_translate("MainWindow", "Set Input"))
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
        self.pushButton_6.setText(_translate("MainWindow", "Set Input"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.pushButton_7.setText(_translate("MainWindow", "Save data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "FFT Tab"))
        self.pushButton.setText(_translate("MainWindow", "Linearization"))
        self.pushButton_2.setText(_translate("MainWindow", "Cumsum flattening"))
        self.pushButton_3.setText(_translate("MainWindow", "Chip calib"))
        self.pushButton_4.setText(_translate("MainWindow", "Set Input"))
        self.toolButton_calib.setText(_translate("MainWindow", "..."))
        self.toolButton_linear.setText(_translate("MainWindow", "..."))
        self.toolButton_flat.setText(_translate("MainWindow", "..."))
        self.label_scope_IP.setText(_translate("MainWindow", "Scope IP"))
        self.label_naive_connect.setText(_translate("MainWindow", "Native connect"))
        self.label_iters.setText(_translate("MainWindow", "# of iterations/vector"))
        self.label_slice_ignore.setText(_translate("MainWindow", "Slices to ignore"))
        self.label_sub_pulse_times.setText(_translate("MainWindow", "Sub pulses"))
        self.label_target_freq.setText(_translate("MainWindow", "Target frequency"))
        self.label_set_scope.setText(_translate("MainWindow", "Set scope:"))
        self.label_scope_scale.setText(_translate("MainWindow", "time"))
        self.label_scope_delay.setText(_translate("MainWindow", "delay"))
        self.label_lin_file_name.setText(_translate("MainWindow", "Llin file"))
        self.label_by_D2S.setText(_translate("MainWindow", "Calib by D2S"))
        self.label_V0.setText(_translate("MainWindow", "V0"))
        self.label_Kd.setText(_translate("MainWindow", "Kd"))
        self.label_Kp.setText(_translate("MainWindow", "Kp"))
        self.label_Ki.setText(_translate("MainWindow", "Ki"))
        self.label_flat_file_name.setText(_translate("MainWindow", "Flat file"))
        self.label_Vbias.setText(_translate("MainWindow", "Vbias"))
        self.label_GM_DAC.setText(_translate("MainWindow", "GM_DAC"))
        self.label_AMP_ATT.setText(_translate("MainWindow", "AMP_ATT"))
        self.label_set_scope_2.setText(_translate("MainWindow", "Set scope:"))
        self.label_scope_scale_2.setText(_translate("MainWindow", "time"))
        self.label_scope_delay_2.setText(_translate("MainWindow", "delay"))
        self.label_calib_file_name.setText(_translate("MainWindow", "Calib file"))
        self.label_lin_dat.setText(_translate("MainWindow", "Linearization"))
        self.label_cums_dat.setText(_translate("MainWindow", "Flattening"))
        self.label_chip_dat.setText(_translate("MainWindow", "Chip Calibration"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Calib Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def lin_getfiles(self):        
        # fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        # if fname[0]:
        #     f = open(fname[0], 'r')

        #     with f:
        #         data = f.read()
        #         self.lin_file_name.setText(data) 


        lin_fl, _ = QFileDialog.getOpenFileName(self, "Select Exel File",
                                            filter="TXT files (*.txt)")
        self.lin_file_name.setText(lin_fl) 

    def flat_getfiles(self): 

        flat_fl, _ = QFileDialog.getOpenFileName(self, "Select Exel File",
                                            filter="TXT files (*.txt)")
        self.flat_file_name.setText(flat_fl)  

    def calib_getfiles(self): 

        calib_fl, _ = QFileDialog.getOpenFileName(self, "Select Exel File",
                                            filter="Exel files (*.xlsx)")
        self.calib_file_name.setText(calib_fl)       

    def setInput(self):
        if not self.scope_IP.text() or not \
            self.naive_connect.text() or not \
            self.iters.text() or not \
            self.slice_ignore.text() or not \
            self.sub_pulse_times.text() or not \
            self.target_freq.text() or not \
            self.scope_scale.text() or not \
            self.scope_delay.text() or not \
            self.lin_file_name.text() or not \
            self.by_D2S.text() or not \
            self.V0.text() or not \
            self.Kd.text() or not \
            self.Kp.text() or not \
            self.Ki.text() or not \
            self.flat_file_name.text() or not \
            self.Vbias.text() or not \
            self.GM_DAC.text() or not \
            self.AMP_ATT.text() or not \
            self.scope_scale_2.text() or not \
            self.scope_delay_2.text() or not \
            self.calib_file_name.text():
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Critical)
            alert.setText("Please enter all values")
            alert.setWindowTitle("Input Error")
            alert.exec_()
            #print("Please enter all three values")
        else:
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat)
            
    def collect_calib_data(self):
        self.Mainwin.calib_dat.naive_connect = int(self.naive_connect.text())
        self.Mainwin.calib_dat.iters = self.iters.text()
        self.Mainwin.calib_dat.slice_ignore = self.slice_ignore.text()
        self.Mainwin.calib_dat.sub_pulse_times = self.sub_pulse_times.text()
        self.Mainwin.calib_dat.target_freq = float(self.target_freq.text())
        self.Mainwin.calib_dat.target_freq = "{:.2e}".format(self.Mainwin.calib_dat.target_freq)
        self.Mainwin.calib_dat.lin_dat.scope_scale = float(self.scope_scale.text())
        self.Mainwin.calib_dat.lin_dat.scope_scale = "{:.2e}".format(self.Mainwin.calib_dat.lin_dat.scope_scale)
        self.Mainwin.calib_dat.lin_dat.scope_delay = float(self.scope_delay.text())
        self.Mainwin.calib_dat.lin_dat.scope_delay = "{:.2e}".format(self.Mainwin.calib_dat.lin_dat.scope_delay)
        self.Mainwin.calib_dat.lin_dat.file_name = self.lin_file_name.text()

        self.Mainwin.calib_dat.by_D2S = self.by_D2S.text()
        self.Mainwin.calib_dat.V0 = int(self.V0.text())
        self.Mainwin.calib_dat.Kd = float(self.Kd.text())
        self.Mainwin.calib_dat.Kp = float(self.Kp.text())
        self.Mainwin.calib_dat.Kp = "{:.2e}".format(self.Mainwin.calib_dat.Kp)
        self.Mainwin.calib_dat.Ki = float(self.Ki.text())
        self.Mainwin.calib_dat.cums_dat.file_name = self.flat_file_name.text()

        self.Mainwin.calib_dat.Vbias = float(self.Vbias.text())
        self.Mainwin.calib_dat.Vbias = "{:.2e}".format(self.Mainwin.calib_dat.Vbias)
        self.Mainwin.calib_dat.GM_DAC = int(self.GM_DAC.text())
        self.Mainwin.calib_dat.AMP_ATT = int(self.AMP_ATT.text())
        self.Mainwin.calib_dat.chip_dat.scope_scale = float(self.scope_scale_2.text())
        self.Mainwin.calib_dat.chip_dat.scope_scale = "{:.2e}".format(self.Mainwin.calib_dat.chip_dat.scope_scale)
        self.Mainwin.calib_dat.chip_dat.scope_delay = float(self.scope_delay_2.text())
        self.Mainwin.calib_dat.chip_dat.scope_delay = "{:.2e}".format(self.Mainwin.calib_dat.chip_dat.scope_delay)
        self.Mainwin.calib_dat.chip_dat.file_name = self.calib_file_name.text()

        print(self.Mainwin.calib_dat.naive_connect,self.Mainwin.calib_dat.iters,self.Mainwin.calib_dat.slice_ignore,self.Mainwin.calib_dat.sub_pulse_times,self.Mainwin.calib_dat.target_freq,self.Mainwin.calib_dat.lin_dat.scope_scale,self.Mainwin.calib_dat.lin_dat.scope_delay,self.Mainwin.calib_dat.lin_dat.file_name)

    @QtCore.pyqtSlot(bool)
    def linear(self,checked):
        if checked:
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.rowOverride = True
            self.Mainwin.calib_dat.but_state.lin_but=1
            self.Mainwin.calib_dat.but_state.cums_but=0
            self.Mainwin.calib_dat.but_state.chip_but=0
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat)           
        elif not checked:
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.rowOverride = False
            self.Mainwin.calib_dat.but_state.lin_but=0
            self.Mainwin.calib_dat.but_state.cums_but=0
            self.Mainwin.calib_dat.but_state.chip_but=0
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat) 

    def flat(self,checked):
        if checked:
            self.pushButton.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.rowOverride = True
            self.Mainwin.calib_dat.but_state.lin_but=0
            self.Mainwin.calib_dat.but_state.cums_but=1
            self.Mainwin.calib_dat.but_state.chip_but=0
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat) 
        elif not checked:
            self.pushButton.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.rowOverride = False
            self.Mainwin.calib_dat.but_state.lin_but=0
            self.Mainwin.calib_dat.but_state.cums_but=0
            self.Mainwin.calib_dat.but_state.chip_but=0
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat) 

    def calib(self,checked):
        if checked:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.rowOverride = True
            self.Mainwin.calib_dat.but_state.lin_but=0
            self.Mainwin.calib_dat.but_state.cums_but=0
            self.Mainwin.calib_dat.but_state.chip_but=1
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat)
        elif not checked:
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.rowOverride = False  
            self.Mainwin.calib_dat.but_state.lin_but=0
            self.Mainwin.calib_dat.but_state.cums_but=0
            self.Mainwin.calib_dat.but_state.chip_but=0
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat) 

    def update_from_qus(self):
        print("111")
        q_empty=1
        counter=0
        # while 1:
        print('q in timer reached')
        # time.sleep(1)
        q_empty=self.ques.Q_calib_output.qsize()==0
        print('q_empty= %d' % q_empty)

        if not q_empty:
            print('q is full in timer')
            try:
                self.Mainwin.cal_dat_out = self.ques.Q_calib_output.get(False)
                print('got data!!')
                print(vars(self.Mainwin.cal_dat_out))
                # aa=vars(cal_dat_out)
                if hasattr(self.Mainwin.cal_dat_out,'cums_graph') == True:
                    # self.graphicsView = CumsumError_Update(self.tab_2, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                    # self.graphicsView = CumsumError_Update(self.tab_2, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                    # self.graphicsView.move(470,400) 
                    CumsumError_Update(self.graphicsView_Cumsum, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                #if hasattr(cal_dat_out,'vco_graph') == True:


            except:
                print("no data in Q_calib_output",self.ques.Q_calib_output.qsize())
                q_empty=1
                pass     

        #*******************change to Q_FFT_output
        if not q_empty:
            print('q is full in timer')
            try:
                self.Mainwin.cal_dat_out = self.ques.Q_calib_output.get(False)
                print('got data!!')
                print(vars(self.Mainwin.cal_dat_out))
                # aa=vars(cal_dat_out)
                if hasattr(self.Mainwin.cal_dat_out,'cums_graph') == True:
                    # self.graphicsView = CumsumError_Update(self.tab_2, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                    # self.graphicsView = CumsumError_Update(self.tab_2, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                    # self.graphicsView.move(470,400) 
                    CumsumError_Update(self.graphicsView_Cumsum, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                #if hasattr(cal_dat_out,'vco_graph') == True:


            except:
                print("no data in Q_calib_output",self.ques.Q_calib_output.qsize())
                q_empty=1
                pass      

                #*******************change to Q_state_out
        if not q_empty:
            print('q is full in timer')
            try:
                self.Mainwin.cal_dat_out = self.ques.Q_calib_output.get(False)
                print('got data!!')
                print(vars(self.Mainwin.cal_dat_out))
                # aa=vars(cal_dat_out)
                if hasattr(self.Mainwin.cal_dat_out,'cums_graph') == True:
                    # self.graphicsView = CumsumError_Update(self.tab_2, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                    # self.graphicsView = CumsumError_Update(self.tab_2, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                    # self.graphicsView.move(470,400) 
                    CumsumError_Update(self.graphicsView_Cumsum, width=3.5, height=3.5,cal_dat_out=self.Mainwin.cal_dat_out)
                #if hasattr(cal_dat_out,'vco_graph') == True:


            except:
                print("no data in Q_calib_output",self.ques.Q_calib_output.qsize())
                q_empty=1
                pass       
        # q_empty=1
        # counter+=1

#class startParams():

    #def __init__(self,): 
        #self.scope_IP = QtWidgets.QLineEdit(self)       
        # self.my_dat=queue_data_classes.calib_input_data()
        #Fill in fields
        # print(self.my_dat.scope_IP)
        # print(self.naive_connect.text())
        # print(self.Vbias.text())
        # print(self.GM_DAC.text())
        # print(self.AMP_ATT.text())
        # print(self.scope_delay.text())
        # print(self.scope_scale.text())
        # print(self.calib_file_name.text())

class VCO(FigureCanvas):  

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
 
    def plot(self):
        data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(data, 'r-')
        ax.set_title('VCO display')
        self.draw()  

class Linearization(FigureCanvas):  

    def __init__(self, parent=None, width=4.5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.timePlot()   

    def timePlot(self):
        #Open csv file
        filename="Start.csv"
        file = open(filename, "r")
        data = [row for row in csv.reader(file)]
        file.close()


        # Data for plotting
        x_start = data[4][1]
        y_start = data[4][2]
        x_stop = data[4][3]
        y_stop = data[4][4]
        x = np.arange(int(x_start), int(y_start), 0.1)
        y = 1 + np.sin(2 * np.pi * x)
        #y = np.arange(int(y_start), int(y_stop), 0.01)

        ax = self.figure.add_subplot(111)
        ax.plot(x, y, 'r-')
        #ax.plot(data, 'r-')
        #ax.set(xlabel='time (s)', ylabel='voltage (mV)',title='Time domain')
        ax.set_title('Linearization')
        self.draw() 

class CumsumError(FigureCanvas):  

    def __init__(self, parent=None, width=4.5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.timePlot()   

    def timePlot(self):
 
        #Open csv file
        filename="Start.csv"
        file = open(filename, "r")
        data = [row for row in csv.reader(file)]
        file.close()

        # Data for plotting
        x_start = data[5][1]
        y_start = data[5][2]
        x_stop = data[5][3]
        y_stop = data[5][4]
        x = np.arange(int(x_start), int(y_start), 0.1)
        y = 1 + np.sin(2 * np.pi * x)
        #y = np.arange(int(y_start), int(y_stop), 0.01)

        self.ax = self.figure.add_subplot(111)
        self.ax.plot(x, y, 'r-')
        #ax.plot(data, 'r-')
        #ax.set(xlabel='time (s)', ylabel='voltage (mV)',title='Time domain')
        self.ax.set_title('Cumsum error')
        self.draw() 

    def updateData(self):
        if not hasattr(self, 'line'):
            # this should only be executed on the first call to updateData
            self.ui.graph.axes.clear()
            self.ui.graph.axes.hold(True)
            self.line = self.ui.graph.axes.plot(self.ValueTotal,'r-')
            self.ui.graph.axes.grid()
        else:
            # now we only modify the plotted line
            self.line.set_xdata(np.arange(len(self.ValueTotal))
            self.line.set_ydata(self.ValueTotal)
        self.ui.graph.draw()    

class CumsumError_Update():  

    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginWidget(self)
        self.login_widget.button.clicked.connect(self.plotter)
        self.central_widget.addWidget(self.login_widget)

    def plotter(self):
        self.data =[0]
        self.curve = self.login_widget.plot.getPlotItem().plot()

        self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.updater)
        # self.timer.start(0)
        self.timer.timeout.connect(lambda: self.update_from_qus())
        self.timer.start(10000) 

    def updater(self):

        self.data.append(self.data[-1]+0.2*(0.5-random.random()) )
        self.curve.setData(self.data)    

    # def __init__(self, parent=None, width=4.5, height=4, dpi=100, cal_dat_out=[]):
    #     plt.ion()
    #     # fig = Figure(figsize=(width, height), dpi=dpi)
    #     # self.axes = fig.add_subplot(111)

    #     # FigureCanvas.__init__(self, fig)
    #     # self.setParent(parent)

    #     # FigureCanvas.setSizePolicy(self,
    #     #         QSizePolicy.Expanding,
    #     #         QSizePolicy.Expanding)
    #     # FigureCanvas.updateGeometry(self)
    #     self.view=parent
    #     self.timePlot(cal_dat_out.cums_graph)   

    # def timePlot(self,graph_dat):    

    #     # Data for plotting
    #     # x_start = self.Mainwin.cal_dat_out.graph_data.xdat
    #     # y_start = self.Mainwin.cal_dat_out.graph_data.ydat
    #     # x_stop = self.Mainwin.cal_dat_out.graph_data.xlim
    #     # y_stop = self.Mainwin.cal_dat_out.graph_data.ylim
    #     # ylog = self.Mainwin.cal_dat_out.graph_data.ylog
    #     x = graph_dat.xdat
    #     y = graph_dat.ydat
    #     #y = np.arange(int(y_start), int(y_stop), 0.01)
    #     # self.view.axes=self.view.figure.axes
    #     self.view.axes.cla()  # clear the axes content
    #     #plt.sca(self.view.axes)
    #     self.view.axes.clear()
    #     # graphicView.ax = self.figure.add_subplot(111)
    #     self.view.axes.plot(x, y, 'r-')
    #     plt.xlim(graph_dat.xlim[0],graph_dat.xlim[1])
    #     plt.ylim(graph_dat.ylim[0],graph_dat.ylim[1])
    #     if graph_dat.ylog==1:
    #         plt.yscale('log')
    #     else:
    #         plt.yscale('linear')
    #     #ax.plot(data, 'r-')
    #     #ax.set(xlabel='time (s)', ylabel='voltage (mV)',title='Time domain')
    #     # self.view.axes.set_title('Cumsum error')
    #     # self.view.fig.canvas.draw_idle()
    #     ani = animation.FuncAnimation(fig, animate, interval=1000)
    #     self.plt.pause(dpause)
    #     self.plt.canvas.draw()()
 
class OneBit(FigureCanvas):  

    def __init__(self, parent=None, width=4.5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.timePlot()   

    def timePlot(self):
        #Open csv file
        filename="Start.csv"
        file = open(filename, "r")
        data = [row for row in csv.reader(file)]
        file.close()

        # Data for plotting
        x_start = data[6][1]
        y_start = data[6][2]
        x_stop = data[6][3]
        y_stop = data[6][4]
        x = np.arange(int(x_start), int(y_start), 0.1)
        y = 1 + np.sin(2 * np.pi * x)
        #y = np.arange(int(y_start), int(y_stop), 0.01)

        ax = self.figure.add_subplot(111)
        ax.plot(x, y, 'r-')
        #ax.plot(data, 'r-')
        #ax.set(xlabel='time (s)', ylabel='voltage (mV)',title='Time domain')
        ax.set_title('1bit average')
        self.draw() 

class TimeDomain(FigureCanvas):  

    def __init__(self, parent=None, width=4.5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.timePlot()   

    def timePlot(self):
        #Open csv file
        filename="Start.csv"
        file = open(filename, "r")
        data = [row for row in csv.reader(file)]

        # Data for plotting
        x_start = data[1][1]
        y_start = data[1][2]
        x_stop = data[1][3]
        y_stop = data[1][4]
        x = np.arange(int(x_start), int(y_start), 0.1)
        y = 1 + np.sin(2 * np.pi * x)
        #y = np.arange(int(y_start), int(y_stop), 0.01)

        ax = self.figure.add_subplot(111)
        ax.plot(x, y, 'r-')
        #ax.plot(data, 'r-')
        #ax.set(xlabel='time (s)', ylabel='voltage (mV)',title='Time domain')
        ax.set_title('Time domain')
        self.draw() 

class FFTDisp(FigureCanvas):  

    def __init__(self, parent=None, width=4.5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.fftPlot()   

    def fftPlot(self):
        #Open csv file
        filename="Start.csv"
        file = open(filename, "r")
        data = [row for row in csv.reader(file)]

        # Data for plotting
        x_start = data[2][1]
        y_start = data[2][2]
        x_stop = data[2][3]
        y_stop = data[2][4]
        y_scale_log = data[2][5]
        x = np.arange(int(x_start), int(y_start), 0.1)
        #x = np.arange(int(x_start), int(y_start), int(y_scale_log))
        y = 1 + np.sin(2 * np.pi * x)
        #y = np.arange(int(y_start), int(y_stop), 0.01)

        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        #ax.plot(data, 'r-')
        #ax.set(xlabel='time (s)', ylabel='voltage (mV)',title='Time domain')
        ax.set_title('Main FFT display')
        self.draw() 

    # def loadCsv(self, fileName):
    #     df_time=pd.read_csv(input("Enter Gold Exel filemane and path: "))
    #     with open(fileName, "r") as fileInput:
    #         for row in csv.reader(fileInput):    
    #             items = [QtGui.QStandardItem(field) for field in row]
    #             self.model.appendRow(items) 

    # def magic(self,n):
    #     n = int(n)
    #     if n < 3:
    #         raise ValueError("Size must be at least 3")
    #     if n % 2 == 1:
    #         p = np.arange(1, n+1)
    #         return n*np.mod(p[:, None] + p - (n+3)//2, n) + np.mod(p[:, None] + 2*p-2, n) + 1
    #     elif n % 4 == 0:
    #         J = np.mod(np.arange(1, n+1), 4) // 2
    #         K = J[:, None] == J
    #         M = np.arange(1, n*n+1, n)[:, None] + np.arange(n)
    #         M[K] = n*n + 1 - M[K]
    #     else:
    #         p = n//2
    #         M = magic(p)
    #         M = np.block([[M, M+2*p*p], [M+3*p*p, M+p*p]])
    #         i = np.arange(p)
    #         k = (n-2)//4
    #         j = np.concatenate((np.arange(k), np.arange(n-k+1, n)))
    #         M[np.ix_(np.concatenate((i, i+p)), j)] = M[np.ix_(np.concatenate((i+p, i)), j)]
    #         M[np.ix_([k, k+p], [0, k])] = M[np.ix_([k+p, k], [0, k])]
    #     return M 

    # x = np.arange(0,10)
    # mm=magic(10,20)
    # y = np.sin(x)
    # z=np.random.rand(10,3)  
    # plt.plot(x, y)
    # plt.plot(x, z)

    # plt.show()            