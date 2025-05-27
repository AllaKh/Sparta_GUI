from __future__ import division
import sys

from lablayout2 import *

from PyQt4.QtGui import *

from PyQt4.QtCore import *

import pyqtgraph as pg

from pyqtgraph.Point import Point

from pyqtgraph.Qt import QtGui, QtCore

import numpy as np

import gc

import random

import serial

import re

import csv

import matplotlib as ml



class MyForm(QtGui.QMainWindow):

    plotUpdating = 0

    i=0

    data=[]

    nl=0

    nq=0

    s = serial.Serial('COM3',9600,timeout=1)

    buffer = ''

    def __init__(self,parent=None):

        QtGui.QWidget.__init__(self,parent)

        self.ui = Ui_MainWindow()

        self.ui.setupUi(self)

        self.graph = self.ui.graphicsView.getPlotItem()

        #self.graph2 = self.ui.graphicsView.getPlotItem()

        self.graph.showGrid(x=True, y=True, alpha=None)

        self.graph.addLegend()

        self.updatePlot()

        self.timer = QtCore.QTimer(self)

        self.connect(self.ui.actionStartData, QtCore.SIGNAL('triggered()')

        ,self.startData)

        self.connect(self.ui.actionStopData, QtCore.SIGNAL('triggered()')

        ,self.stopData)

        self.connect(self.ui.actionExit_Application,QtCore.SIGNAL('triggered()')

        ,self.quitApplication)

        self.connect(self.ui.actionOpen,QtCore.SIGNAL('triggered()')

        ,self.openFile)

        self.connect(self.ui.actionSave,QtCore.SIGNAL('triggered()')

        ,self.saveFile)

        self.connect(self.ui.actionQuadratic, QtCore.SIGNAL('triggered()')

        ,self.quadraticFit)

        self.connect(self.ui.actionLinear, QtCore.SIGNAL('changed()')

        ,self.linearFit)

        self.connect(self.ui.action3rd_order, QtCore.SIGNAL('triggered()')

        ,self.thirdFit)

        self.connect(self.ui.action4th_order, QtCore.SIGNAL('triggered()')

        ,self.fourthFit)

        self.connect(self.ui.action5th_order, QtCore.SIGNAL('triggered()')

        ,self.fifthFit)

        self.connect(self.ui.statisticsButton, QtCore.SIGNAL('clicked()')

        ,self.updateStatistics)

        self.graph.scene().sigMouseMoved.connect(self.mouseMoved)

        self.ui.textBrowser.append('Statistics')

        # Used for the crosshairs in the plot...

        self.vLine = pg.InfiniteLine(angle=90, movable=False)

        self.hLine = pg.InfiniteLine(angle=0, movable=False)

            

        self.proxy = pg.SignalProxy(self.graph.scene().sigMouseMoved, rateLimit=10

        , slot=self.mouseMoved)