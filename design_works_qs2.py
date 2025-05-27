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

import csv
import random
from ximea import xiapi
import cv2
import sys

import queue_data_classes
import pyqtgraph as pg

class Ui_MainWindow(object):
    def __init__(self):
        self.iter_counter=0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_from_qus)
        # noinspection PyArgumentList
        self.timer.start(800)
    
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
        self.graphicsView_5 = QtWidgets.QGraphicsView(self.tab)
        self.graphicsView_5.setGeometry(QtCore.QRect(10, 20, 401, 361))
        self.graphicsView_5.setObjectName("graphicsView_5")
        # self.graphicsView_5 = Camera(self.tab, width=4.5, height=4)
        # self.graphicsView_5.move(0,0)

        #Cursor position
        self.label_cursor = QtWidgets.QLabel(self.tab)
        self.label_cursor.setGeometry(QtCore.QRect(20, 410, 81, 21))
        self.label_cursor.setObjectName("label_cursor")
        self.cursor = QtWidgets.QLineEdit(self.tab)
        self.cursor.setGeometry(QtCore.QRect(100, 410, 141, 20))
        self.cursor.setObjectName("cursor")
        self.cursor.setText(str(self.Mainwin.fft_dat.camera_cursor_pos)) 

        #Set Input Cursor position
        self.pushButton_5 = QtWidgets.QPushButton(self.tab)
        self.pushButton_5.setGeometry(QtCore.QRect(290, 400, 111, 41))
        self.pushButton_5.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.pushButton_5.setObjectName("pushButton_5")

        #Time domain      
        self.time_widget = pg.GraphicsLayoutWidget(self.tab)
        self.time_widget.setGeometry(QtCore.QRect(10, 460, 401, 381))

        self.time_pl = self.time_widget.addPlot(title="Time domain")
        self.time_pl.setDownsampling(mode='peak')
        self.time_pl.setClipToView(True)
        self.time_pl.addLegend()
        self.time_d =[0]
        self.time_d.append(1)
        self.time_d.append(2)
        self.time_curve = self.time_pl.plot()
        self.time_curve.setData(self.time_d)   

        self.line_2 = QtWidgets.QFrame(self.tab)
        self.line_2.setGeometry(QtCore.QRect(420, 20, 20, 821))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        #X lims
        self.label_X_lims = QtWidgets.QLabel(self.tab)
        self.label_X_lims.setGeometry(QtCore.QRect(490, 20, 41, 31))
        self.label_X_lims.setObjectName("label_X_lims")
        self.X_lims = QtWidgets.QLineEdit(self.tab)
        self.X_lims.setGeometry(QtCore.QRect(440, 50, 141, 31))
        self.X_lims.setObjectName("X_lims")
        self.X_lims.setText(str(self.Mainwin.fft_dat.xlim)) 

        #Y lims
        self.label_Y_lims = QtWidgets.QLabel(self.tab)
        self.label_Y_lims.setGeometry(QtCore.QRect(490, 90, 41, 31))
        self.label_Y_lims.setObjectName("label_Y_lims")
        self.Y_lims = QtWidgets.QLineEdit(self.tab)
        self.Y_lims.setGeometry(QtCore.QRect(440, 120, 141, 31))
        self.Y_lims.setObjectName("Y_lims")
        self.Y_lims.setText(str(self.Mainwin.fft_dat.ylim))

        #Y log
        self.label_ylog = QtWidgets.QLabel(self.tab)
        self.label_ylog.setGeometry(QtCore.QRect(490, 160, 47, 14))
        self.label_ylog.setObjectName("label_ylog")
        self.ylog = QtWidgets.QLineEdit(self.tab)
        self.ylog.setGeometry(QtCore.QRect(440, 180, 141, 31))
        self.ylog.setObjectName("ylog")        
        self.ylog.setText(str(self.Mainwin.fft_dat.ylog))

        #N chirps
        self.label_N_chirps = QtWidgets.QLabel(self.tab)
        self.label_N_chirps.setGeometry(QtCore.QRect(490, 220, 47, 14))
        self.label_N_chirps.setObjectName("label_N_chirps")
        self.N_chirps = QtWidgets.QLineEdit(self.tab)
        self.N_chirps.setGeometry(QtCore.QRect(440, 240, 141, 31))
        self.N_chirps.setObjectName("N_chirps")
        self.N_chirps.setText(str(self.Mainwin.fft_dat.Nchirps))

        self.line_3 = QtWidgets.QFrame(self.tab)
        self.line_3.setGeometry(QtCore.QRect(430, 280, 161, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")

        # Analisis
        self.label_Analisis = QtWidgets.QLabel(self.tab)
        self.label_Analisis.setGeometry(QtCore.QRect(490, 310, 47, 14))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_Analisis.setFont(font)        
        self.label_Analisis.setObjectName("label_Analisis")

        self.radioButton_mean = QtWidgets.QRadioButton(self.tab)
        self.radioButton_mean.setGeometry(QtCore.QRect(450, 340, 74, 18))
        self.radioButton_mean.setObjectName("radioButton_mean")
        self.radioButton_mean.toggled.connect(self.btnstate)

        self.radioButton_STD = QtWidgets.QRadioButton(self.tab)
        self.radioButton_STD.setGeometry(QtCore.QRect(450, 360, 74, 18))
        self.radioButton_STD.setObjectName("radioButton_STD")
        self.radioButton_STD.setChecked(True)
        self.radioButton_STD.toggled.connect(self.btnstate)

        self.radioButton_max = QtWidgets.QRadioButton(self.tab)
        self.radioButton_max.setGeometry(QtCore.QRect(450, 380, 74, 18))
        self.radioButton_max.setObjectName("radioButton_max")
        self.radioButton_max.toggled.connect(self.btnstate)

        self.radioButton_min = QtWidgets.QRadioButton(self.tab)
        self.radioButton_min.setGeometry(QtCore.QRect(450, 400, 74, 18))
        self.radioButton_min.setObjectName("radioButton_min")     
        self.radioButton_min.toggled.connect(self.btnstate)

        self.line_4 = QtWidgets.QFrame(self.tab)
        self.line_4.setGeometry(QtCore.QRect(430, 430, 161, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")

        #SNR
        self.label_SNR = QtWidgets.QLabel(self.tab)
        self.label_SNR.setGeometry(QtCore.QRect(490, 450, 47, 14))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_SNR.setFont(font)
        self.label_SNR.setObjectName("label_SNR")

        #Noise freqs
        self.label_noise = QtWidgets.QLabel(self.tab)
        self.label_noise.setGeometry(QtCore.QRect(480, 480, 61, 16))
        self.label_noise.setObjectName("label_noise")
        self.noise = QtWidgets.QLineEdit(self.tab)
        self.noise.setGeometry(QtCore.QRect(440, 500, 141, 31))
        self.noise.setObjectName("noise")
        self.noise.setText(str(self.Mainwin.fft_dat.noise_freqs))

        #Peak freqs
        self.label_signal = QtWidgets.QLabel(self.tab)
        self.label_signal.setGeometry(QtCore.QRect(480, 550, 51, 16))
        self.label_signal.setObjectName("label_signal")
        self.signal = QtWidgets.QLineEdit(self.tab)
        self.signal.setGeometry(QtCore.QRect(440, 580, 141, 31))
        self.signal.setObjectName("signal")
        self.signal.setText(str(self.Mainwin.fft_dat.peak_freqs))

        self.line_5 = QtWidgets.QFrame(self.tab)
        self.line_5.setGeometry(QtCore.QRect(430, 630, 161, 16))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self.tab)
        self.line_6.setGeometry(QtCore.QRect(583, 20, 20, 821))
        self.line_6.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")

        #Set scope label
        self.label_set_scope_FFT = QtWidgets.QLabel(self.tab)
        self.label_set_scope_FFT.setGeometry(QtCore.QRect(480, 650, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_set_scope_FFT.setFont(font)
        self.label_set_scope_FFT.setObjectName("label_set_scope_FFT")

        #time
        self.label_scope_scale_FFT = QtWidgets.QLabel(self.tab)
        self.label_scope_scale_FFT.setGeometry(QtCore.QRect(440, 680, 31, 16))
        self.label_scope_scale_FFT.setObjectName("label_scope_scale_FFT")
        self.scope_scale_FFT = QtWidgets.QLineEdit(self.tab)
        self.scope_scale_FFT.setGeometry(QtCore.QRect(480, 680, 101, 20))
        self.scope_scale_FFT.setObjectName("scope_scale_FFT")
        self.scope_scale_FFT.setText("{:.2e}".format(self.Mainwin.fft_dat.scope_scale))

        #delay
        self.label_scope_delay_FFT = QtWidgets.QLabel(self.tab)
        self.label_scope_delay_FFT.setGeometry(QtCore.QRect(440, 720, 31, 16))
        self.label_scope_delay_FFT.setObjectName("label_scope_delay_FFT")
        self.scope_delay_FFT = QtWidgets.QLineEdit(self.tab)
        self.scope_delay_FFT.setGeometry(QtCore.QRect(480, 720, 101, 20))
        self.scope_delay_FFT.setObjectName("scope_delay_FFT")
        self.scope_delay_FFT.setText("{:.2e}".format(self.Mainwin.fft_dat.scope_delay))

        #Set Input
        self.pushButton_6 = QtWidgets.QPushButton(self.tab)
        self.pushButton_6.setGeometry(QtCore.QRect(444, 780, 131, 61))
        self.pushButton_6.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.setInput_fft)

        #Main FFT display
        self.fft_widget = pg.GraphicsLayoutWidget(self.tab)
        self.fft_widget.setGeometry(QtCore.QRect(600, 10, 511, 701))

        self.fft_pl = self.fft_widget.addPlot(title="Main FFT display")
        self.fft_pl.setDownsampling(mode='peak')
        self.fft_pl.setClipToView(True)
        self.fft_pl.addLegend()
        self.fft_d =[0]
        self.fft_d.append(1)
        self.fft_d.append(2)
        self.fft_curve = self.fft_pl.plot()
        self.fft_curve.setData(self.fft_d)   

        #Save
        self.save_data = QtWidgets.QLineEdit(self.tab)
        self.save_data.setGeometry(QtCore.QRect(610, 788, 281, 51))
        self.save_data.setObjectName("save_data")
        self.save_data.setText(str(self.Mainwin.fft_dat.save_path))
        self.toolButton_save = QtWidgets.QToolButton(self.tab)
        self.toolButton_save.setGeometry(QtCore.QRect(900, 798, 51, 31))
        self.toolButton_save.setObjectName("toolButton_save")
        self.toolButton_save.clicked.connect(self.save_getfiles)        
        #self.toolButton.clicked.connect(self.browse_folder)
        self.pushButton_save = QtWidgets.QPushButton(self.tab)
        self.pushButton_save.setGeometry(QtCore.QRect(960, 780, 141, 61))
        self.pushButton_save.setStyleSheet("background-color: rgb(170, 170, 255);")
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.setStatusTip('Save File')
        self.pushButton_save.clicked.connect(self.file_save)

        self.tabWidget.addTab(self.tab, "")

        # Create second tab 
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")

        #Linearization button
        self.pushButton = QtWidgets.QPushButton(self.tab_2)
        self.pushButton.setGeometry(QtCore.QRect(40, 120, 111, 61))
        self.pushButton.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCheckable(True)
        self.pushButton.toggled.connect(self.linear)

        #Cumsum flattening button
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(40, 250, 111, 61))
        self.pushButton_2.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.toggled.connect(self.flat)        

        #Chip calib button
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_3.setGeometry(QtCore.QRect(40, 390, 111, 61))
        self.pushButton_3.setStyleSheet("background-color: rgb(170, 255, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.toggled.connect(self.calib)          

        #Scope IP and Sparta IP
        self.label_scope_IP = QtWidgets.QLabel(self.tab_2)
        self.label_scope_IP.setGeometry(QtCore.QRect(220, 10, 61, 16))
        self.label_scope_IP.setObjectName("label_scope_IP")
        self.scope_IP = QtWidgets.QLineEdit(self.tab_2)
        self.scope_IP.setGeometry(QtCore.QRect(350, 10, 113, 20))
        self.scope_IP.setObjectName("scope_IP")
        self.scope_IP.setText(self.Mainwin.calib_dat.scope_IP)

        self.label_sparta_IP = QtWidgets.QLabel(self.tab_2)
        self.label_sparta_IP.setGeometry(QtCore.QRect(220, 30, 81, 16))
        self.label_sparta_IP.setObjectName("label_sparta_IP")
        self.sparta_IP = QtWidgets.QLineEdit(self.tab_2)
        self.sparta_IP.setGeometry(QtCore.QRect(350, 30, 113, 20))
        self.sparta_IP.setObjectName("sparta_IP")
        self.sparta_IP.setText(str(self.Mainwin.calib_dat.sparta_IP))

        #linearization: # iterations
        self.label_lin_dat = QtWidgets.QLabel(self.tab_2)
        self.label_lin_dat.setGeometry(QtCore.QRect(310, 70, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_lin_dat.setFont(font)
        self.label_lin_dat.setObjectName("label_lin_dat")   

        #Nchirps
        self.label_Nchirps = QtWidgets.QLabel(self.tab_2)
        self.label_Nchirps.setGeometry(QtCore.QRect(220, 100, 41, 16))
        self.label_Nchirps.setObjectName("label_Nchirps")
        self.Nchirps = QtWidgets.QLineEdit(self.tab_2)
        self.Nchirps.setGeometry(QtCore.QRect(270, 100, 51, 20))
        self.Nchirps.setObjectName("Nchirps")  
        self.Nchirps.setText(str(self.Mainwin.calib_dat.lin_dat.Nchirps))

        #Nchirps to average
        self.label_Nchirps_to_average = QtWidgets.QLabel(self.tab_2)
        self.label_Nchirps_to_average.setGeometry(QtCore.QRect(330, 100, 81, 16))
        self.label_Nchirps_to_average.setObjectName("label_Nchirps_to_average")
        self.Nchirps_to_average = QtWidgets.QLineEdit(self.tab_2)
        self.Nchirps_to_average.setGeometry(QtCore.QRect(410, 100, 51, 20))
        self.Nchirps_to_average.setObjectName("Nchirps_to_average")    
        self.Nchirps_to_average.setText(str(self.Mainwin.calib_dat.lin_dat.Nchirps_to_average))

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

        #BW range
        self.label_BW_range = QtWidgets.QLabel(self.tab_2)
        self.label_BW_range.setGeometry(QtCore.QRect(220, 190, 71, 16))
        self.label_BW_range.setObjectName("label_BW_range")
        self.BW_range = QtWidgets.QLineEdit(self.tab_2)
        self.BW_range.setGeometry(QtCore.QRect(350, 160, 113, 20))
        self.BW_range.setObjectName("slice_ignore")
        self.BW_range.setText(str(self.Mainwin.calib_dat.lin_dat.BW_range))

        #number of sub pulses
        self.label_sub_pulse_times = QtWidgets.QLabel(self.tab_2)
        self.label_sub_pulse_times.setGeometry(QtCore.QRect(220, 220, 71, 16))
        self.label_sub_pulse_times.setObjectName("label_sub_pulse_times")
        self.sub_pulse_times = QtWidgets.QLineEdit(self.tab_2)
        self.sub_pulse_times.setGeometry(QtCore.QRect(350, 220, 113, 20))
        self.sub_pulse_times.setObjectName("sub_pulse_times")
        self.sub_pulse_times.setText(str(self.Mainwin.calib_dat.lin_dat.sub_pulse_times))

        #target center frequency
        self.label_target_freq = QtWidgets.QLabel(self.tab_2)
        self.label_target_freq.setGeometry(QtCore.QRect(220, 250, 91, 16))
        self.label_target_freq.setObjectName("label_target_freq")
        self.target_freq = QtWidgets.QLineEdit(self.tab_2)
        self.target_freq.setGeometry(QtCore.QRect(350, 250, 113, 20))
        self.target_freq.setObjectName("target_freq")
        self.target_freq.setText("{:.2e}".format(self.Mainwin.calib_dat.lin_dat.target_freq))

        #set scope time and time delay
        self.label_set_scope_lin = QtWidgets.QLabel(self.tab_2)
        self.label_set_scope_lin.setGeometry(QtCore.QRect(220, 280, 61, 20))
        self.label_set_scope_lin.setObjectName("label_set_scope_lin")
        self.label_scope_scale_lin = QtWidgets.QLabel(self.tab_2)
        self.label_scope_scale_lin.setGeometry(QtCore.QRect(280, 280, 31, 16))
        self.label_scope_scale_lin.setObjectName("label_scope_scale_lin")
        self.scope_scale_lin = QtWidgets.QLineEdit(self.tab_2)
        self.scope_scale_lin.setGeometry(QtCore.QRect(310, 280, 51, 20))
        self.scope_scale_lin.setObjectName("scope_scale_lin")
        self.scope_scale_lin.setText("{:.2e}".format(self.Mainwin.calib_dat.lin_dat.scope_scale))

        self.label_scope_delay_lin = QtWidgets.QLabel(self.tab_2)
        self.label_scope_delay_lin.setGeometry(QtCore.QRect(380, 280, 31, 16))
        self.label_scope_delay_lin.setObjectName("label_scope_delay_lin")
        self.scope_delay_lin = QtWidgets.QLineEdit(self.tab_2)
        self.scope_delay_lin.setGeometry(QtCore.QRect(410, 280, 51, 20))
        self.scope_delay_lin.setObjectName("scope_delay_lin")
        self.scope_delay_lin.setText("{:.2e}".format(self.Mainwin.calib_dat.lin_dat.scope_delay))

        #lin file name
        self.label_lin_file_name = QtWidgets.QLabel(self.tab_2)
        self.label_lin_file_name.setGeometry(QtCore.QRect(220, 310, 47, 14))
        self.label_lin_file_name.setObjectName("label_lin_file_name")
        self.lin_file_name = QtWidgets.QLineEdit(self.tab_2)
        self.lin_file_name.setGeometry(QtCore.QRect(280, 310, 113, 20))
        self.lin_file_name.setObjectName("lin_file_name")
        self.lin_file_name.setText(self.Mainwin.calib_dat.lin_dat.file_name)

        self.toolButton_linear = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_linear.setGeometry(QtCore.QRect(420, 310, 23, 20))
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
        self.label_by_D2S.setGeometry(QtCore.QRect(220, 380, 71, 16))
        self.label_by_D2S.setObjectName("label_by_D2S")
        self.by_D2S = QtWidgets.QLineEdit(self.tab_2)
        self.by_D2S.setGeometry(QtCore.QRect(350, 380, 113, 20))
        self.by_D2S.setObjectName("by_D2S")
        self.by_D2S.setText(str(self.Mainwin.calib_dat.cums_dat.by_D2S))

        #V0 
        self.label_V0 = QtWidgets.QLabel(self.tab_2)
        self.label_V0.setGeometry(QtCore.QRect(220, 410, 21, 16))
        self.label_V0.setObjectName("label_V0")
        self.V0 = QtWidgets.QLineEdit(self.tab_2)
        self.V0.setGeometry(QtCore.QRect(280, 410, 51, 20))
        self.V0.setObjectName("V0")
        self.V0.setText(str(self.Mainwin.calib_dat.cums_dat.V0))

        #Kd
        self.label_Kd = QtWidgets.QLabel(self.tab_2)
        self.label_Kd.setGeometry(QtCore.QRect(390, 410, 21, 16))
        self.label_Kd.setObjectName("label_Kd")
        self.Kd = QtWidgets.QLineEdit(self.tab_2)
        self.Kd.setGeometry(QtCore.QRect(410, 410, 51, 20))
        self.Kd.setObjectName("Kd")
        self.Kd.setText(str(self.Mainwin.calib_dat.cums_dat.Kd))

        #Kp
        self.label_Kp = QtWidgets.QLabel(self.tab_2)
        self.label_Kp.setGeometry(QtCore.QRect(220, 440, 21, 16))
        self.label_Kp.setObjectName("label_Kp")
        self.Kp = QtWidgets.QLineEdit(self.tab_2)
        self.Kp.setGeometry(QtCore.QRect(280, 440, 51, 20))
        self.Kp.setObjectName("Kp")
        self.Kp.setText("{:.2e}".format(self.Mainwin.calib_dat.cums_dat.Kp))

        #Ki
        self.label_Ki = QtWidgets.QLabel(self.tab_2)
        self.label_Ki.setGeometry(QtCore.QRect(390, 440, 21, 16))
        self.label_Ki.setObjectName("label_Ki")
        self.Ki = QtWidgets.QLineEdit(self.tab_2)
        self.Ki.setGeometry(QtCore.QRect(410, 440, 51, 20))
        self.Ki.setObjectName("Ki")
        self.Ki.setText(str(self.Mainwin.calib_dat.cums_dat.Ki))

        #Err min
        self.label_err_min = QtWidgets.QLabel(self.tab_2)
        self.label_err_min.setGeometry(QtCore.QRect(220, 470, 41, 16))
        self.label_err_min.setObjectName("label_err_min")
        self.err_min = QtWidgets.QLineEdit(self.tab_2)
        self.err_min.setGeometry(QtCore.QRect(280, 470, 51, 20))
        self.err_min.setObjectName("err_min")
        self.err_min.setText(str(self.Mainwin.calib_dat.cums_dat.err_min))

        #Smooth win
        self.label_smooth_win = QtWidgets.QLabel(self.tab_2)
        self.label_smooth_win.setGeometry(QtCore.QRect(340, 470, 61, 16))
        self.label_smooth_win.setObjectName("label_smooth_win")
        self.smooth_win = QtWidgets.QLineEdit(self.tab_2)
        self.smooth_win.setGeometry(QtCore.QRect(410, 470, 51, 20))
        self.smooth_win.setObjectName("smooth_win")
        self.smooth_win.setText(str(self.Mainwin.calib_dat.cums_dat.smooth_win))

        #0 offset ind
        self.label_first_correction_ind = QtWidgets.QLabel(self.tab_2)
        self.label_first_correction_ind.setGeometry(QtCore.QRect(220, 500, 61, 16))
        self.label_first_correction_ind.setObjectName("label_first_correction_ind")
        self.first_correction_ind = QtWidgets.QLineEdit(self.tab_2)
        self.first_correction_ind.setGeometry(QtCore.QRect(280, 500, 51, 20))
        self.first_correction_ind.setObjectName("first_correction_ind")
        self.first_correction_ind.setText(str(self.Mainwin.calib_dat.cums_dat.first_correction_ind))

        #Flat. crit.
        self.label_flatness_crit = QtWidgets.QLabel(self.tab_2)
        self.label_flatness_crit.setGeometry(QtCore.QRect(360, 500, 51, 16))
        self.label_flatness_crit.setObjectName("label_flatness_crit")
        self.flatness_crit = QtWidgets.QLineEdit(self.tab_2)
        self.flatness_crit.setGeometry(QtCore.QRect(410, 500, 51, 20))
        self.flatness_crit.setObjectName("flatness_crit")
        self.flatness_crit.setText(str(self.Mainwin.calib_dat.cums_dat.flatness_crit))

        #Cor. start time
        self.label_Tos = QtWidgets.QLabel(self.tab_2)
        self.label_Tos.setGeometry(QtCore.QRect(220, 530, 81, 16))
        self.label_Tos.setObjectName("label_Tos")
        self.Tos = QtWidgets.QLineEdit(self.tab_2)
        self.Tos.setGeometry(QtCore.QRect(350, 530, 111, 20))
        self.Tos.setObjectName("Tos")
        self.Tos.setText("{:.2e}".format(self.Mainwin.calib_dat.cums_dat.Tos))

        #Set scope
        self.label_set_scope_flat = QtWidgets.QLabel(self.tab_2)
        self.label_set_scope_flat.setGeometry(QtCore.QRect(220, 560, 61, 20))
        self.label_set_scope_flat.setObjectName("label_set_scope_flat")

        self.label_scope_scale_flat = QtWidgets.QLabel(self.tab_2)
        self.label_scope_scale_flat.setGeometry(QtCore.QRect(290, 560, 31, 16))
        self.label_scope_scale_flat.setObjectName("label_scope_scale_flat")
        self.scope_scale_flat = QtWidgets.QLineEdit(self.tab_2)
        self.scope_scale_flat.setGeometry(QtCore.QRect(320, 560, 51, 20))
        self.scope_scale_flat.setObjectName("scope_scale_flat")
        self.scope_scale_flat.setText("{:.2e}".format(self.Mainwin.calib_dat.cums_dat.scope_scale))

        self.label_scope_delay_flat = QtWidgets.QLabel(self.tab_2)
        self.label_scope_delay_flat.setGeometry(QtCore.QRect(380, 560, 31, 16))
        self.label_scope_delay_flat.setObjectName("label_scope_delay_flat")
        self.scope_delay_flat = QtWidgets.QLineEdit(self.tab_2)
        self.scope_delay_flat.setGeometry(QtCore.QRect(410, 560, 51, 20))
        self.scope_delay_flat.setObjectName("scope_delay_flat")
        self.scope_delay_flat.setText("{:.2e}".format(self.Mainwin.calib_dat.cums_dat.scope_delay))

        #flat file
        self.label_flat_file_name = QtWidgets.QLabel(self.tab_2)
        self.label_flat_file_name.setGeometry(QtCore.QRect(220, 590, 41, 16))
        self.label_flat_file_name.setObjectName("label_flat_file_name")
        self.flat_file_name = QtWidgets.QLineEdit(self.tab_2)
        self.flat_file_name.setGeometry(QtCore.QRect(280, 590, 113, 20))
        self.flat_file_name.setObjectName("flat_file_name")
        self.flat_file_name.setText(self.Mainwin.calib_dat.cums_dat.file_name)

        self.toolButton_flat = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_flat.setGeometry(QtCore.QRect(420, 590, 23, 20))
        self.toolButton_flat.setObjectName("toolButton_flat")
        self.toolButton_flat.clicked.connect(self.flat_getfiles)

        #Chip calibration
        self.label_chip_dat = QtWidgets.QLabel(self.tab_2)
        self.label_chip_dat.setGeometry(QtCore.QRect(310, 640, 101, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_chip_dat.setFont(font)
        self.label_chip_dat.setObjectName("label_chip_dat")

        #Vbias
        self.label_Vbias = QtWidgets.QLabel(self.tab_2)
        self.label_Vbias.setGeometry(QtCore.QRect(220, 670, 31, 16))
        self.label_Vbias.setObjectName("label_Vbias")
        self.Vbias = QtWidgets.QLineEdit(self.tab_2)
        self.Vbias.setGeometry(QtCore.QRect(350, 670, 113, 20))
        self.Vbias.setObjectName("Vbias")
        self.Vbias.setText("{:.2e}".format(self.Mainwin.calib_dat.chip_dat.Vbias))       

        # #GM_DAC
        # self.label_GM_DAC = QtWidgets.QLabel(self.tab_2)
        # self.label_GM_DAC.setGeometry(QtCore.QRect(220, 620, 51, 16))
        # self.label_GM_DAC.setObjectName("label_GM_DAC")
        # self.GM_DAC = QtWidgets.QLineEdit(self.tab_2)
        # self.GM_DAC.setGeometry(QtCore.QRect(350, 620, 113, 20))
        # self.GM_DAC.setObjectName("GM_DAC")
        # self.GM_DAC.setText(str(self.Mainwin.calib_dat.chip_dat.GM_DAC)) 

        # #AMP_ATT
        # self.label_AMP_ATT = QtWidgets.QLabel(self.tab_2)
        # self.label_AMP_ATT.setGeometry(QtCore.QRect(220, 650, 61, 16))
        # self.label_AMP_ATT.setObjectName("label_AMP_ATT")
        # self.AMP_ATT = QtWidgets.QLineEdit(self.tab_2)
        # self.AMP_ATT.setGeometry(QtCore.QRect(350, 650, 113, 20))
        # self.AMP_ATT.setObjectName("AMP_ATT")
        # self.AMP_ATT.setText(str(self.Mainwin.calib_dat.chip_dat.AMP_ATT)) 

        #Set scope
        self.label_set_scope_chip = QtWidgets.QLabel(self.tab_2)
        self.label_set_scope_chip.setGeometry(QtCore.QRect(220, 700, 61, 20))
        self.label_set_scope_chip.setObjectName("label_set_scope_chip")
        self.label_scope_scale_chip = QtWidgets.QLabel(self.tab_2)
        self.label_scope_scale_chip.setGeometry(QtCore.QRect(290, 700, 31, 16))
        self.label_scope_scale_chip.setObjectName("label_scope_scale_chip")
        self.scope_scale_chip = QtWidgets.QLineEdit(self.tab_2)
        self.scope_scale_chip.setGeometry(QtCore.QRect(320, 700, 51, 20))
        self.scope_scale_chip.setObjectName("scope_scale_chip")
        self.scope_scale_chip.setText("{:.2e}".format(self.Mainwin.calib_dat.chip_dat.scope_scale))  

        self.label_scope_delay_chip = QtWidgets.QLabel(self.tab_2)
        self.label_scope_delay_chip.setGeometry(QtCore.QRect(380, 700, 31, 16))
        self.label_scope_delay_chip.setObjectName("label_scope_delay_chip")
        self.scope_delay_chip = QtWidgets.QLineEdit(self.tab_2)
        self.scope_delay_chip.setGeometry(QtCore.QRect(410, 700, 51, 20))
        self.scope_delay_chip.setObjectName("scope_delay_chip")
        self.scope_delay_chip.setText("{:.2e}".format(self.Mainwin.calib_dat.chip_dat.scope_delay)) 

        #calib file
        self.label_calib_file_name = QtWidgets.QLabel(self.tab_2)
        self.label_calib_file_name.setGeometry(QtCore.QRect(220, 730, 47, 14))
        self.label_calib_file_name.setObjectName("label_calib_file_name")
        self.calib_file_name = QtWidgets.QLineEdit(self.tab_2)
        self.calib_file_name.setGeometry(QtCore.QRect(290, 730, 113, 20))
        self.calib_file_name.setObjectName("calib_file_name")
        self.calib_file_name.setText(self.Mainwin.calib_dat.chip_dat.file_name)

        self.toolButton_calib = QtWidgets.QToolButton(self.tab_2)
        self.toolButton_calib.setGeometry(QtCore.QRect(430, 730, 23, 20))
        self.toolButton_calib.setObjectName("toolButton_calib")
        self.toolButton_calib.clicked.connect(self.calib_getfiles)

        #Sheet name
        self.label_sheet_name = QtWidgets.QLabel(self.tab_2)
        self.label_sheet_name.setGeometry(QtCore.QRect(220, 760, 61, 16))
        self.label_sheet_name.setObjectName("label_sheet_name")
        self.sheet_name = QtWidgets.QLineEdit(self.tab_2)
        self.sheet_name.setGeometry(QtCore.QRect(350, 760, 113, 20))
        self.sheet_name.setObjectName("sheet_name")
        self.sheet_name.setText(self.Mainwin.calib_dat.chip_dat.sheet_name)

        # Set Calib Input button
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(250, 800, 151, 41))
        self.pushButton_4.setStyleSheet("background-color: rgb(170, 255, 0);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.setInput)

        self.line = QtWidgets.QFrame(self.tab_2)
        self.line.setGeometry(QtCore.QRect(190, 40, 20, 811))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        #VCO display 
        self.vco_widget = pg.GraphicsLayoutWidget(self.tab_2)
        self.vco_widget.setGeometry(QtCore.QRect(490, 30, 300, 300))
        
        self.vco_pl = self.vco_widget.addPlot(title="VCO display")
        self.vco_pl.setDownsampling(mode='peak')
        self.vco_pl.setClipToView(True)
        self.vco_pl.addLegend()
        self.vco_d =[0]
        self.vco_d.append(1)
        self.vco_d.append(2)
        self.vco_curve = self.vco_pl.plot()
        self.vco_curve.setData(self.vco_d)   

        #Linearization 
        self.linear_widget = pg.GraphicsLayoutWidget(self.tab_2)
        self.linear_widget.setGeometry(QtCore.QRect(800, 30, 300, 300))
        
        self.linear_pl = self.linear_widget.addPlot(title="Linearization")
        self.linear_pl.setDownsampling(mode='peak')
        self.linear_pl.setClipToView(True)
        self.linear_pl.addLegend()
        self.linear_d =[0]
        self.linear_d.append(1)
        self.linear_d.append(2)
        self.linear_curve = self.linear_pl.plot()
        self.linear_curve.setData(self.linear_d)            

        #Cumsum error
        self.сumsum_widget = pg.GraphicsLayoutWidget(self.tab_2)
        self.сumsum_widget.setGeometry(QtCore.QRect(490, 430, 300, 300))
        
        self.сumsum_pl = self.сumsum_widget.addPlot(title="Cumsum error")
        self.сumsum_pl.setDownsampling(mode='peak')
        self.сumsum_pl.setClipToView(True)
        self.сumsum_pl.addLegend()
        self.сumsum_d =[0]
        self.сumsum_d.append(1)
        self.сumsum_d.append(2)
        self.сumsum_curve = self.сumsum_pl.plot()
        self.сumsum_curve.setData(self.сumsum_d)            

        #1bit average 
        self.onebit_widget = pg.GraphicsLayoutWidget(self.tab_2)
        self.onebit_widget.setGeometry(QtCore.QRect(800, 430, 300, 300))
        
        self.onebit_pl = self.onebit_widget.addPlot(title="1bit average")
        self.onebit_pl.setDownsampling(mode='peak')
        self.onebit_pl.setClipToView(True)
        self.onebit_pl.addLegend()
        self.onebit_d =[0]
        self.onebit_d.append(1)
        self.onebit_d.append(2)
        self.onebit_curve = self.onebit_pl.plot()
        self.onebit_curve.setData(self.onebit_d)     

        #main window and menu
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
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setObjectName("actionSave")
        self.actionSave.setStatusTip('Save File')
        self.actionSave.triggered.connect(self.file_save)
        self.actionSave_as = QtWidgets.QAction(self.Mainwin)
        self.actionSave_as.setShortcut("Ctrl+Shift+S")
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave_as.setStatusTip('Choose file to save')
        self.actionSave_as.triggered.connect(self.file_save)
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
        self.label_cursor.setText(_translate("MainWindow", "Cursor position"))
        self.pushButton_5.setText(_translate("MainWindow", "Set Input"))
        self.label_X_lims.setText(_translate("MainWindow", "X lims"))
        self.label_Y_lims.setText(_translate("MainWindow", "Y lims"))
        self.label_ylog.setText(_translate("MainWindow", "Y log"))        
        self.label_N_chirps.setText(_translate("MainWindow", "N chirps"))
        self.label_Analisis.setText(_translate("MainWindow", "Analysis:"))
        self.radioButton_mean.setText(_translate("MainWindow", "mean"))
        self.radioButton_STD.setText(_translate("MainWindow", "STD"))
        self.radioButton_max.setText(_translate("MainWindow", "max"))
        self.radioButton_min.setText(_translate("MainWindow", "min"))
        self.label_SNR.setText(_translate("MainWindow", "SNR"))
        self.label_noise.setText(_translate("MainWindow", "Noise bin range"))
        self.label_signal.setText(_translate("MainWindow", "Signal bin range"))
        self.label_scope_delay_FFT.setText(_translate("MainWindow", "delay"))
        self.label_scope_scale_FFT.setText(_translate("MainWindow", "time"))
        self.label_set_scope_FFT.setText(_translate("MainWindow", "Set scope:"))
        self.pushButton_6.setText(_translate("MainWindow", "Set Input"))
        self.toolButton_save.setText(_translate("MainWindow", "..."))
        self.pushButton_save.setText(_translate("MainWindow", "Save data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "FFT Tab"))
        self.pushButton.setText(_translate("MainWindow", "Linearization"))
        self.pushButton_2.setText(_translate("MainWindow", "Cumsum flattening"))
        self.pushButton_3.setText(_translate("MainWindow", "Chip calib"))
        self.pushButton_4.setText(_translate("MainWindow", "Set Input"))
        self.toolButton_calib.setText(_translate("MainWindow", "..."))
        self.toolButton_linear.setText(_translate("MainWindow", "..."))
        self.toolButton_flat.setText(_translate("MainWindow", "..."))
        self.label_scope_IP.setText(_translate("MainWindow", "Scope IP"))
        self.label_sparta_IP.setText(_translate("MainWindow", "Sparta IP"))
        self.label_iters.setText(_translate("MainWindow", "# of iterations/vector"))
        self.label_slice_ignore.setText(_translate("MainWindow", "Slices to ignore"))
        self.label_BW_range.setText(_translate("MainWindow", "BW range"))
        self.label_target_freq.setText(_translate("MainWindow", "Target Frequency"))
        self.label_set_scope_lin.setText(_translate("MainWindow", "Set scope:"))
        self.label_scope_scale_lin.setText(_translate("MainWindow", "time"))
        self.label_scope_delay_lin.setText(_translate("MainWindow", "delay"))
        self.label_lin_file_name.setText(_translate("MainWindow", "Llin file"))
        self.label_by_D2S.setText(_translate("MainWindow", "Calib by D2S"))
        self.label_V0.setText(_translate("MainWindow", "V0"))
        self.label_Kd.setText(_translate("MainWindow", "Kd"))
        self.label_Kp.setText(_translate("MainWindow", "Kp"))
        self.label_Ki.setText(_translate("MainWindow", "Ki"))
        self.label_flat_file_name.setText(_translate("MainWindow", "Flat file"))
        self.label_Vbias.setText(_translate("MainWindow", "Vbias"))
        self.label_sheet_name.setText(_translate("MainWindow", "Sheet Name"))
        self.label_set_scope_chip.setText(_translate("MainWindow", "Set scope:"))
        self.label_scope_scale_chip.setText(_translate("MainWindow", "time"))
        self.label_scope_delay_chip.setText(_translate("MainWindow", "delay"))
        self.label_calib_file_name.setText(_translate("MainWindow", "Calib file"))
        self.label_lin_dat.setText(_translate("MainWindow", "Linearization"))
        self.label_cums_dat.setText(_translate("MainWindow", "Flattening"))
        self.label_chip_dat.setText(_translate("MainWindow", "Chip Calibration"))
        self.label_scope_scale_flat.setText(_translate("MainWindow", "time"))
        self.label_scope_delay_flat.setText(_translate("MainWindow", "delay"))
        self.label_set_scope_flat.setText(_translate("MainWindow", "Set scope:"))
        self.label_smooth_win.setText(_translate("MainWindow", "Smooth win."))
        self.label_err_min.setText(_translate("MainWindow", "Err min"))
        self.label_flatness_crit.setText(_translate("MainWindow", "Flat. crit."))
        self.label_first_correction_ind.setText(_translate("MainWindow", "0 offset ind"))
        self.label_sub_pulse_times.setText(_translate("MainWindow", "Sub pulse times"))
        self.label_Nchirps.setText(_translate("MainWindow", "Nchirps"))
        self.label_Nchirps_to_average.setText(_translate("MainWindow", "Nchirps to ave."))
        self.label_Tos.setText(_translate("MainWindow", "Cor. start time"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Calib Tab 2"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))

    def save_getfiles(self):        

        save_fl, _ = QFileDialog.getOpenFileName(self, "Select Exel File",
                                            filter="Exel files (*.csv)")
        self.save_data.setText(save_fl) 

    def file_save(self):
        name = QFileDialog.getOpenFileName(self, "Select Exel File",
                                            filter="Exel files (*.csv)")
        file = open(name,'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()

    def btnstate(self):
        self.analysis=0
        if self.radioButton_mean.isChecked()==True:
            self.analysis=0
            print(self.analysis)
        if self.radioButton_STD.isChecked()==True:
            self.analysis=1
            print(self.analysis)
        if self.radioButton_max.isChecked()==True:
            self.analysis=2
            print(self.analysis)
        if self.radioButton_min.isChecked()==True:
            self.analysis=3
            print(self.analysis)
        return self.analysis

    def lin_getfiles(self):        
        # fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        # if fname[0]:
        #     f = open(fname[0], 'r')

        #     with f:
        #         data = f.read()
        #         self.lin_file_name.setText(data) 


        lin_fl, _ = QFileDialog.getOpenFileName(self, "Select text File",
                                            filter="TXT files (*.txt)")
        self.lin_file_name.setText(lin_fl) 

    def flat_getfiles(self): 

        flat_fl, _ = QFileDialog.getOpenFileName(self, "Select text File",
                                            filter="TXT files (*.txt)")
        self.flat_file_name.setText(flat_fl)  

    def calib_getfiles(self): 

        calib_fl, _ = QFileDialog.getOpenFileName(self, "Select Exel File",
                                            filter="Exel files (*.xlsx)")
        self.calib_file_name.setText(calib_fl)       

    def setInput_fft(self):
        if not self.X_lims.text() or not \
            self.Y_lims.text() or not \
            self.ylog.text() or not \
            self.N_chirps.text() or not \
            self.noise.text() or not \
            self.signal.text() or not \
            self.scope_scale_FFT.text() or not \
            self.scope_delay_FFT.text():
            alert = QMessageBox()
            alert.setIcon(QMessageBox.Critical)
            alert.setText("Please enter all values")
            alert.setWindowTitle("Input Error")
            alert.exec_()
            #print("Please enter all three values")
        else:
            self.collect_fft_data()
            self.ques.Q_FFT_input.put(self.Mainwin.fft_dat)
            
    def collect_fft_data(self):
        #self.Mainwin.fft_dat.camera_cursor_pos = int(self.cursor.text())
        self.Mainwin.fft_dat.xlim = self.X_lims.text()
        self.Mainwin.fft_dat.ylim = self.Y_lims.text()
        self.Mainwin.fft_dat.ylog = self.ylog.text()
        self.Mainwin.fft_dat.analysis_type = self.btnstate()
        self.Mainwin.fft_dat.noise_freqs = self.noise.text()
        self.Mainwin.fft_dat.peak_freqs = self.signal.text()
        self.Mainwin.fft_dat.scope_scale = float(self.scope_scale_FFT.text())
        self.Mainwin.fft_dat.scope_delay = float(self.scope_delay_FFT.text())
        #self.Mainwin.fft_dat.save_path = self.save_data.text()

        print(self.Mainwin.fft_dat.xlim,self.Mainwin.fft_dat.ylim,self.Mainwin.fft_dat.ylog,self.Mainwin.fft_dat.analysis_type,self.Mainwin.fft_dat.noise_freqs,self.Mainwin.fft_dat.peak_freqs,self.Mainwin.fft_dat.scope_delay,self.Mainwin.fft_dat.scope_scale)

    def setInput(self):
        if not self.scope_IP.text() or not \
            self.sparta_IP.text() or not \
            self.Nchirps or not \
            self.Nchirps_to_average or not \
            self.iters.text() or not \
            self.slice_ignore.text() or not \
            self.BW_range or not \
            self.sub_pulse_times.text() or not \
            self.target_freq.text() or not \
            self.scope_scale_lin.text() or not \
            self.scope_delay_lin.text() or not \
            self.lin_file_name.text() or not \
            self.by_D2S.text() or not \
            self.V0.text() or not \
            self.Kd.text() or not \
            self.Kp.text() or not \
            self.Ki.text() or not \
            self.err_min.text() or not \
            self.smooth_win.text() or not \
            self.first_correction_ind.text() or not \
            self.flatness_crit.text() or not \
            self.Tos.text() or not \
            self.scope_scale_flat.text() or not \
            self.scope_delay_flat.text() or not \
            self.flat_file_name.text() or not \
            self.Vbias.text() or not \
            self.scope_scale_chip.text() or not \
            self.scope_delay_chip.text() or not \
            self.sheet_name.text() or not \
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
        self.Mainwin.calib_dat.scope_IP = self.scope_IP.text()
        self.Mainwin.calib_dat.sparta_IP = self.sparta_IP.text()
        self.Mainwin.calib_dat.lin_dat.iters = self.iters.text()
        self.Mainwin.calib_dat.lin_dat.Nchirps = int(self.Nchirps.text())
        self.Mainwin.calib_dat.lin_dat.Nchirps_to_average = int(self.Nchirps_to_average.text())
        self.Mainwin.calib_dat.lin_dat.slice_ignore = self.slice_ignore.text()
        self.Mainwin.calib_dat.lin_dat.BW_range = self.BW_range.text()
        self.Mainwin.calib_dat.lin_dat.sub_pulse_times = np.asarray([float(i) for i in self.sub_pulse_times.text()])
        self.Mainwin.calib_dat.lin_dat.target_freq = float(self.target_freq.text())
        # self.Mainwin.calib_dat.target_freq = "{:.2e}".format(self.Mainwin.calib_dat.target_freq)
        self.Mainwin.calib_dat.lin_dat.scope_scale = float(self.scope_scale_lin.text())
        # self.Mainwin.calib_dat.lin_dat.scope_scale = "{:.2e}".format(self.Mainwin.calib_dat.lin_dat.scope_scale)
        self.Mainwin.calib_dat.lin_dat.scope_delay = float(self.scope_delay_lin.text())
        # self.Mainwin.calib_dat.lin_dat.scope_delay = "{:.2e}".format(self.Mainwin.calib_dat.lin_dat.scope_delay)
        self.Mainwin.calib_dat.lin_dat.file_name = self.lin_file_name.text()

        self.Mainwin.calib_dat.cums_dat.by_D2S = self.by_D2S.text()
        self.Mainwin.calib_dat.cums_dat.V0 = int(self.V0.text())
        self.Mainwin.calib_dat.cums_dat.Kd = float(self.Kd.text())
        self.Mainwin.calib_dat.cums_dat.Kp = float(self.Kp.text())
        # self.Mainwin.calib_dat.Kp = "{:.2e}".format(self.Mainwin.calib_dat.Kp)
        self.Mainwin.calib_dat.cums_dat.Ki = float(self.Ki.text())
        self.Mainwin.calib_dat.cums_dat.err_min = float(self.err_min.text())
        self.Mainwin.calib_dat.cums_dat.smooth_win = int(self.smooth_win.text())
        self.Mainwin.calib_dat.cums_dat.first_correction_ind = int(self.first_correction_ind.text())
        self.Mainwin.calib_dat.cums_dat.flatness_crit = float(self.flatness_crit.text())
        self.Mainwin.calib_dat.cums_dat.Tos = float(self.Tos.text())
        self.Mainwin.calib_dat.cums_dat.scope_scale = float(self.scope_scale_flat.text())
        self.Mainwin.calib_dat.cums_dat.scope_delay = float(self.scope_delay_flat.text())
        self.Mainwin.calib_dat.cums_dat.file_name = self.flat_file_name.text()

        self.Mainwin.calib_dat.chip_dat.Vbias = float(self.Vbias.text())
        # self.Mainwin.calib_dat.chip_dat.GM_DAC = int(self.GM_DAC.text())
        # self.Mainwin.calib_dat.chip_dat.AMP_ATT = int(self.AMP_ATT.text())
        self.Mainwin.calib_dat.chip_dat.scope_scale = float(self.scope_scale_chip.text())
        # self.Mainwin.calib_dat.chip_dat.scope_scale = "{:.2e}".format(self.Mainwin.calib_dat.chip_dat.scope_scale)
        self.Mainwin.calib_dat.chip_dat.scope_delay = float(self.scope_delay_chip.text())
        # self.Mainwin.calib_dat.chip_dat.scope_delay = "{:.2e}".format(self.Mainwin.calib_dat.chip_dat.scope_delay)
        self.Mainwin.calib_dat.chip_dat.file_name = self.calib_file_name.text()
        self.Mainwin.calib_dat.chip_dat.sheet_name = self.sheet_name.text()
 
        for i in range(len(self.Mainwin.calib_dat.lin_dat.sub_pulse_times)):
            if i%2:        
                self.Mainwin.calib_dat.lin_dat.t_stop_lin.append(self.Mainwin.calib_dat.lin_dat.sub_pulse_times[i])
            else:
                self.Mainwin.calib_dat.lin_dat.t_start_lin.append(self.Mainwin.calib_dat.lin_dat.sub_pulse_times[i])

        print(self.Mainwin.calib_dat.scope_IP,self.Mainwin.calib_dat.sparta_IP,self.Mainwin.calib_dat.lin_dat.iters,self.Mainwin.calib_dat.lin_dat.Nchirps,self.Mainwin.calib_dat.lin_dat.Nchirps_to_average,self.Mainwin.calib_dat.lin_dat.slice_ignore,self.Mainwin.calib_dat.lin_dat.BW_range,self.Mainwin.calib_dat.lin_dat.sub_pulse_times,self.Mainwin.calib_dat.lin_dat.target_freq,self.Mainwin.calib_dat.lin_dat.scope_scale,self.Mainwin.calib_dat.lin_dat.scope_delay,self.Mainwin.calib_dat.lin_dat.file_name,self.Mainwin.calib_dat.cums_dat.Kd,self.Mainwin.calib_dat.cums_dat.Kp,self.Mainwin.calib_dat.cums_dat.Ki,self.Mainwin.calib_dat.cums_dat.err_min,self.Mainwin.calib_dat.cums_dat.smooth_win,self.Mainwin.calib_dat.cums_dat.first_correction_ind,self.Mainwin.calib_dat.cums_dat.flatness_crit,self.Mainwin.calib_dat.cums_dat.Tos,self.Mainwin.calib_dat.cums_dat.scope_scale,self.Mainwin.calib_dat.cums_dat.scope_delay,self.Mainwin.calib_dat.cums_dat.file_name,self.Mainwin.calib_dat.chip_dat.Vbias,self.Mainwin.calib_dat.chip_dat.scope_scale,self.Mainwin.calib_dat.chip_dat.scope_delay,self.Mainwin.calib_dat.chip_dat.file_name,self.Mainwin.calib_dat.chip_dat.sheet_name,self.Mainwin.calib_dat.lin_dat.t_start_lin,self.Mainwin.calib_dat.lin_dat.t_stop_lin)

    @QtCore.pyqtSlot(bool)
    def linear(self,checked):
        if checked:
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)            
            self.rowOverride = True
            self.Mainwin.calib_dat.but_state.lin_but=1
            self.Mainwin.calib_dat.but_state.cums_but=0
            self.Mainwin.calib_dat.but_state.chip_but=0
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat)           
        # elif not checked:
        #     self.pushButton.setEnabled(True)
        #     self.pushButton_2.setEnabled(True)
        #     self.pushButton_3.setEnabled(True)
        #     self.rowOverride = False
        #     self.Mainwin.calib_dat.but_state.lin_but=0
        #     self.Mainwin.calib_dat.but_state.cums_but=0
        #     self.Mainwin.calib_dat.but_state.chip_but=0
        #     self.collect_calib_data()
        #     self.ques.Q_calib_input.put(self.Mainwin.calib_dat) 

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
            self.pushButton_3.setEnabled(False)
            self.rowOverride = True
            self.Mainwin.calib_dat.but_state.lin_but=0
            self.Mainwin.calib_dat.but_state.cums_but=0
            self.Mainwin.calib_dat.but_state.chip_but=1
            self.collect_calib_data()
            self.ques.Q_calib_input.put(self.Mainwin.calib_dat)
        # elif not checked:
        #     self.pushButton.setEnabled(True)
        #     self.pushButton_2.setEnabled(True)
        #     self.pushButton_3.setEnabled(True)
        #     self.rowOverride = False  
        #     self.Mainwin.calib_dat.but_state.lin_but=0
        #     self.Mainwin.calib_dat.but_state.cums_but=0
        #     self.Mainwin.calib_dat.but_state.chip_but=0
        #     self.collect_calib_data()
        #     self.ques.Q_calib_input.put(self.Mainwin.calib_dat) 

    def update_from_qus(self):
        q_empty=1
        fft_q_empty=1
        state_q_empty=1
        self.iter_counter+=1
    
        # print("111")

        # while 1:
        # print('q in timer reached')
        # self.curve.setData(np.random.rand(1000))        
        # time.sleep(1)
        q_empty=self.ques.Q_calib_output.qsize()==0
        # print('q_empty= %d' % q_empty)
        fft_q_empty=self.ques.Q_FFT_output.qsize()==0
        # print('fft_q_empty= %d' % fft_q_empty)
        state_q_empty=self.ques.Q_state_out.qsize()==0
        # print('state_q_empty= %d' % state_q_empty)
        if not self.iter_counter%30:
            print('%d: Q_calib_output empty:%d ;Q_FFT_output=%d; Q_state_out= %d' % (self.iter_counter,q_empty,fft_q_empty,state_q_empty) )

        if not q_empty:
            # print('q is full in timer')
            try:
                self.Mainwin.cal_dat_out = self.ques.Q_calib_output.get(False)
                # print('got data for Q_calib_output!! qsize is',self.ques.Q_state_out.qsize())
                # print(vars(self.Mainwin.cal_dat_out))
                # aa=vars(cal_dat_out)
                if hasattr(self.Mainwin.cal_dat_out,'vco_graph') == True:
                    # print('vco')
                    self.vco_pl.setTitle(self.Mainwin.cal_dat_out.vco_graph.title)
                    self.vco_curve.setData(self.Mainwin.cal_dat_out.vco_graph.xdat,self.Mainwin.cal_dat_out.vco_graph.ydat)                    
                if hasattr(self.Mainwin.cal_dat_out,'lin_graph') == True:
                    # print('lin')
                    self.linear_pl.setTitle(self.Mainwin.cal_dat_out.lin_graph.title)
                    self.linear_curve.setData(self.Mainwin.cal_dat_out.lin_graph.xdat,self.Mainwin.cal_dat_out.lin_graph.ydat)                    
                if hasattr(self.Mainwin.cal_dat_out,'cums_graph') == True:
                    # print('cumsum')
                    self.сumsum_pl.setTitle(self.Mainwin.cal_dat_out.cums_graph.title)
                    self.сumsum_curve.setData(self.Mainwin.cal_dat_out.cums_graph.xdat,self.Mainwin.cal_dat_out.cums_graph.ydat)
                if hasattr(self.Mainwin.cal_dat_out,'oneBit_graph') == True:
                    # print('1bit')
                    self.onebit_pl.setTitle(self.Mainwin.cal_dat_out.oneBit_graph.title)
                    self.onebit_curve.setData(self.Mainwin.cal_dat_out.oneBit_graph.xdat,self.Mainwin.cal_dat_out.oneBit_graph.ydat)
                            
            except:
                # print("no data in Q_calib_output",self.ques.Q_calib_output.qsize())
                q_empty=1
                pass         

        if not state_q_empty:
            # print('state_q is full in timer')
            try:
                self.Mainwin.state_data = self.ques.Q_state_out.get(False)
                # print('got FFT data!!')
                # print(vars(self.Mainwin.cal_dat_out))
                # aa=vars(cal_dat_out)
                if self.Mainwin.state_data.busy:
                    a=5
                    # print("State is busy")
                elif self.Mainwin.calib_dat.but_state.lin_but or self.Mainwin.calib_dat.but_state.chip_but:
                    self.pushButton.setEnabled(True)
                    self.pushButton_2.setEnabled(True)
                    self.pushButton_3.setEnabled(True)
                    self.rowOverride = False
                    self.Mainwin.calib_dat.but_state.lin_but=0
                    self.Mainwin.calib_dat.but_state.cums_but=0
                    self.Mainwin.calib_dat.but_state.chip_but=0 
                    print('calibration has ended, scope released')
                else:
                    print('CLAM on, scope released')
            except:
                # print("no data in Q_fft_input",self.ques.Q_state_out.qsize())
                state_q_empty=1
                pass  

        if not fft_q_empty:
            #self.time_curve.setData(np.random.rand(1000))
            #self.fft_curve.setData(np.random.rand(1000))    
            # print('fft_q is full in timer')
            try:
                self.Mainwin.FFT_dat_out = self.ques.Q_FFT_output.get(False)
                print('got FFT data!!')
                # print(vars(self.Mainwin.cal_dat_out))
                # aa=vars(cal_dat_out)
                if hasattr(self.Mainwin.FFT_dat_out,'fft_graph') == True:
                    # print('fft')
                    self.fft_curve.setData(self.Mainwin.FFT_dat_out.fft_graph.xdat,self.Mainwin.FFT_dat_out.fft_graph.ydat)                    
                if hasattr(self.Mainwin.FFT_dat_out,'time_graph') == True:
                    # print('lin')
                    self.time_curve.setData(self.Mainwin.FFT_dat_out.time_graph.xdat,self.Mainwin.FFT_dat_out.time_graph.ydat)                    
                            
            except:
                # print("no data in Q_FFT_output",self.ques.Q_FFT_output.qsize())
                fft_q_empty=1
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