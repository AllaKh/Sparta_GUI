#! /usr/bin/python

import sys,os

import numpy as np
import datetime,time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg

try:
    import tele
    import connect
    import logger_widget
except:
    from . import tele
    from . import connect
    from . import logger_widget


import pyqtgraph.console

class ControlWidget(QtGui.QWidget):
    def __init__(self):
        super().__init__()
        
        grid_layout = QtGui.QGridLayout()
        vbox_layout = QtGui.QVBoxLayout()
        vbox_layout.addLayout(grid_layout)
        
        self.setLayout(vbox_layout)

        self.button_connect = QtGui.QPushButton("Connect")
        self.button_start   = QtGui.QPushButton("Start")
        self.button_stop    = QtGui.QPushButton("Stop")
        self.ctrl_ip        = QtGui.QLineEdit("127.0.0.1")
        self.ctrl_ver       = QtGui.QLineEdit("---",readOnly=True)
        self.fpga_ver       = QtGui.QLineEdit("---",readOnly=True)
        self.ctrl_ip.setMaximumWidth(100)
        self.ctrl_ip.setFixedWidth(100)
        self.button_connect.setMaximumWidth(100)
        self.button_connect.setFixedWidth(100)
        #text_connect.setFixedWidth(200)
        
        self.button_connect.clicked.connect(lambda:self.on_connect())
        self.button_start.clicked.connect(lambda:self.on_start())
        self.button_stop.clicked.connect(lambda:self.on_stop())

        grid_layout.addWidget(self.ctrl_ip,0,0)
        grid_layout.addWidget(self.button_connect,0,1)
        grid_layout.addWidget(self.button_start,1,0)
        grid_layout.addWidget(self.button_stop,1,1)
        grid_layout.addWidget(QtGui.QLabel("CTRL version"),2,0)
        grid_layout.addWidget(self.ctrl_ver,2,1)
        grid_layout.addWidget(QtGui.QLabel("FPGA version"),3,0)
        grid_layout.addWidget(self.fpga_ver,3,1)
        self.lcd= QtGui.QLCDNumber(5)
        self.lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        grid_layout.addWidget(self.lcd,4,0,4,4)
        
        spacer = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        grid_layout.addItem(spacer)

        self.client=None
    def get_lcd(self):
        return self.lcd

    def  on_connect(self):
        host = self.ctrl_ip.text()
        print("Connect to ",host)
        self.client = connect.SafeCheckIfCtrlUp(host)
        if self.client:
            ver_ctrl = str(self.client.call("GetShortVersion").decode("utf-8")  )  
            ver_fpga = str(self.client.call("GetPlShortVersion",0).decode("utf-8")  )  
            self.ctrl_ver.setText( ver_ctrl)
            self.fpga_ver.setText( ver_fpga)
            if 'dirty' in ver_ctrl :
                self.ctrl_ver.setStyleSheet("color: red;")

    def try_call(self,f,arg):
        if not self.client:
            self.on_connect()
        if self.client :
            try:
                self.client.call(f,*arg)
            except:
                print("Could not rpc, will try to reconect")
                self.on_connect()
                if self.client :
                     self.client.call(f,*arg)


    def  on_start(self):
        self.try_call("Start",[False] )

    def  on_stop(self):
         self.try_call("Stop",[]) 

class App(QtGui.QMainWindow):

    def help(self):
        print('Use this console to execute commands in context of application')

    def rpc(self,f,*arg):
        return self.controlWidget.client.call(f,*arg) 
    
    def __init__(self,app=None):
        super().__init__()
        self.setWindowTitle('Oryx GUI')    
        if app:
            app.aboutToQuit.connect(self.closeAll)
        
        
        self.controlWidget=ControlWidget()

        self.ns = {'app': self,'os':os,'sys':sys,'pg':pg,'np':np,'help':self.help,'rpc':self.rpc}

        self.console = pyqtgraph.console.ConsoleWidget(namespace=self.ns, text="Use app to aceess application data\ni.e. app.setWindowTitle('Test')")

        
        self.tabs     = QtGui.QTabWidget()
        self.console_tab     = self.console
        

        self.logger_tab     = logger_widget.LoggerWidget(self)

        
        

        self.tele_tab = tele.TeleWidget(self.controlWidget.get_lcd())
        # Add tabs
        self.tabs.addTab(self.tele_tab,"Telemetry")
        self.tabs.addTab(self.console_tab,"Script")
        self.tabs.addTab(self.logger_tab,"Logger")

        
        self.main_layout = QtGui.QHBoxLayout()
        
        
        self.main_layout = QtGui.QHBoxLayout()
        
        
        self.main_layout.addWidget(self.tabs)
        self.main_layout.addWidget( self.controlWidget )
        self.main_layout.setStretch(0,90)       
        self.main_layout.setStretch(1,0)
        

        self.setCentralWidget( QtGui.QWidget())
        self.centralWidget().setLayout(self.main_layout)
        self.show()
        self.resize(1100,600)

   

   
    def closeAll(self):
        
        self.tele_tab.close_all()
    
        
            
    

def start(args):
    
    app=    QtGui.QApplication([])
    app.setStyle('Windows')
    gui = App(app)
    app.instance().exec_()


if __name__ == '__main__':
    start(None) 
