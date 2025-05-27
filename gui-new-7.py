import sys,os

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot,pyqtProperty,QObject

import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.console
from pyqtgraph.parametertree import Parameter, ParameterTree

class Ui_MainWindow( QObject):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100,600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.button_set1 = QtWidgets.QPushButton(self.tab)
        self.button_set1.setObjectName("setButton")
        self.button_set1.setMaximumWidth(100)
        self.button_set1.setFixedWidth(100)                 
        self.horizontalLayout.addWidget(self.button_set1)

        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        # self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        # self.gridLayout_4.setObjectName("gridLayout_4")
        # self.gridLayout_4.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")        
        self.linearButton = QtWidgets.QPushButton(self.tab_2)
        self.linearButton.setObjectName("linearButton")
        self.linearButton.setCheckable(True)
        #self.linearButton.clicked[bool].connect(self.setGraph)        
        self.horizontalLayout.addWidget(self.linearButton)

        self.flatButton = QtWidgets.QPushButton(self.tab_2)
        self.flatButton.setObjectName("flatButton")
        self.flatButton.setCheckable(True)
        #self.flatButton.clicked[bool].connect(self.setGraph)        
        self.horizontalLayout.addWidget(self.flatButton)

        self.calibButton = QtWidgets.QPushButton(self.tab_2)
        self.calibButton.setObjectName("calibButton")
        self.calibButton.setCheckable(True)
        #self.calibButton.clicked[bool].connect(self.setGraph)        
        self.horizontalLayout.addWidget(self.calibButton)


        self.label1 = QtWidgets.QLabel(self.tab_2)
        self.label1.setObjectName("linearization: # iterations")
        self.horizontalLayout.addWidget(self.label1)        
        self.textbox1 = QtWidgets.QLineEdit(self.tab_2)
        self.textbox1.setObjectName("# linearization iterations")
        self.horizontalLayout.addWidget(self.textbox1)

        self.label2 = QtWidgets.QLabel(self.tab_2)
        self.label2.setObjectName("Flattening: Vstart, Kp, Ki, Kd")
        self.horizontalLayout.addWidget(self.label2)        
        self.textbox2 = QtWidgets.QLineEdit(self.tab_2)
        self.textbox2.setObjectName("Flatten_params (=[4x1 numpy])")
        self.horizontalLayout.addWidget(self.textbox2)

        self.label3 = QtWidgets.QLabel(self.tab_2)
        self.label3.setObjectName("Chip calib: amp_attenuation")
        self.horizontalLayout.addWidget(self.label3)        
        self.textbox3 = QtWidgets.QLineEdit(self.tab_2)
        self.textbox3.setObjectName("chip_params (=1 numpy)")
        self.horizontalLayout.addWidget(self.textbox3)


        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)

        self.button_set2 = QtWidgets.QPushButton(self.tab_2)
        self.button_set2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.button_set2)

        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        # self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 482, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuQuit = QtWidgets.QMenu(self.menubar)
        self.menuQuit.setObjectName("menuQuit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_Program = QtWidgets.QAction(MainWindow)
        self.actionSave_Program.setObjectName("actionSave_Program")
        self.actionLoad_Program = QtWidgets.QAction(MainWindow)
        self.actionLoad_Program.setObjectName("actionLoad_Program")
        self.menuFile.addAction(self.actionSave_Program)
        self.menuFile.addAction(self.actionLoad_Program)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuQuit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        # self.clearButton.clicked.connect(self.EAXlineEdit.clear)
        # self.pushButton_2.clicked.connect( self.addRandomTextSlot)
        # self.linearButton.clicked.connect(self.textEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button_set1.setText(_translate("MainWindow", "Set input"))      

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Calib Tab"))

        self.linearButton.setText(_translate("MainWindow", "Linearization"))
        self.linearButton.setCheckable(True)

        self.flatButton.setText(_translate("MainWindow", "Cumsum flattening"))
        self.flatButton.setCheckable(True)

        self.calibButton.setText(_translate("MainWindow", "Chip calib"))
        self.calibButton.setCheckable(True)

        # Create labels & textboxes
        self.label1.setText(_translate("MainWindow", "linearization: # iterations"))
        self.label1.setMaximumWidth(100)
        self.label1.setFixedWidth(100)

        self.label2.setText(_translate("MainWindow", "Flattening: Vstart, Kp, Ki, Kd"))
        self.label2.setMaximumWidth(100)
        self.label2.setFixedWidth(100)

        self.label3.setText(_translate("MainWindow", "Chip calib: amp_attenuation"))
        self.label3.setMaximumWidth(100)
        self.label3.setFixedWidth(100)

        self.button_set2.setText(_translate("MainWindow", "Set input"))      
        self.button_set2.setMaximumWidth(100)
        self.button_set2.setFixedWidth(100) 

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "FFT Tab"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuQuit.setTitle(_translate("MainWindow", "Quit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSave_Program.setText(_translate("MainWindow", "Save Program"))
        self.actionLoad_Program.setText(_translate("MainWindow", "Load Program"))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())