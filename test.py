from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtGui import QColor, QIcon
import sys,os

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import pyqtSlot,pyqtProperty

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
        self.clearButton = QtWidgets.QPushButton(self.tab)
        self.clearButton.setObjectName("clearButton")
        self.horizontalLayout.addWidget(self.clearButton)
        self.EAXlineEdit = QtWidgets.QLineEdit(self.tab)
        self.EAXlineEdit.setObjectName("EAXlineEdit")
        self.horizontalLayout.addWidget(self.EAXlineEdit)
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.textEdit = QtWidgets.QTextEdit(self.tab_2)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_4.addWidget(self.textEdit, 0, 0, 1, 1)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.linearButton = QtWidgets.QPushButton(self.tab_2)
        self.linearButton.setObjectName("linearButton")
        self.linearButton.setCheckable(True)
        # self.linearButton.clicked[bool].connect(self.setGraph)        
        self.horizontalLayout_2.addWidget(self.linearButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 1)
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
        self.clearButton.clicked.connect(self.EAXlineEdit.clear)
        self.pushButton_2.clicked.connect( self.addRandomTextSlot)
        self.linearButton.clicked.connect(self.textEdit.clear)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        # self.square =QtGui.QFrame(self)
        # self.square.setGeometry(150, 20, 100, 100)
        # self.square.setStyleSheet("QWidget { background-color: %s }" %
        #     self.col.name())

        self.clearButton.setText(_translate("MainWindow", "Clear"))
        self.label.setText(_translate("MainWindow", "EAX"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "FFT Tab"))
        self.linearButton.setText(_translate("MainWindow", "Linearization"))
        self.pushButton_2.setText(_translate("MainWindow", "Random Text"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Calib Tab"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuQuit.setTitle(_translate("MainWindow", "Quit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSave_Program.setText(_translate("MainWindow", "Save Program"))
        self.actionLoad_Program.setText(_translate("MainWindow", "Load Program"))
    
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
        
    @pyqtSlot( )
    def addRandomTextSlot( self ):
        self.textEdit.insertPlainText( "Hello World!" )

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
