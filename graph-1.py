import sys
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QApplication)
import pyqtgraph as pg
import numpy as np

class CustomPlot(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        # self.x = np.random.normal(size=1000) * 1e-5
        # self.y = self.x * 500 + 0.005 * np.random.normal(size=1000)
        # self.y -= self.y.min() - 1.0
        # self.mask = self.x > 1e-15
        # self.x = self.x[self.mask]
        # self.y = self.y[self.mask]
        # self.plot(self.x, self.y, pen='g', symbol='o', symbolPen='g', symbolSize=1)


        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)

        self.p6 = self.addPlot(title="Updating plot")
        self.curve = p6.plot(pen='y')
        self.data = np.random.normal(size=(10,1000))
        self.ptr = 0
        def update():
            global curve, data, ptr, p6
            self.curve.setData(data[ptr%10])
            if self.ptr == 0:
                self.p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
            self.ptr += 1
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(update)
        self.timer.start(50)

# a class for the second plot to be displayed underneath the first via 
# QVBoxLayout

class CustomPlot1(pg.PlotWidget):
    def __init__(self):
        pg.PlotWidget.__init__(self)
        self.x = np.random.normal(size=1000) * 1e-5 #
        self.y = self.x * 750 + 0.005 * np.random.normal(size=1000)
        self.y -= self.y.min() - 1.0
        self.mask = self.x > 1e-15
        self.x = self.x[self.mask]
        self.y = self.y[self.mask]
        self.plot(self.x, self.y, pen='g', symbol='t', symbolPen='g', symbolSize=1)

# The top container/widget for the graphs
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # call the UI set up

    # set up the UI
    def initUI(self):

        self.layout = QVBoxLayout(self) # create the layout
        self.pgcustom = CustomPlot() # class abstract both the classes
        self.pgcustom1 = CustomPlot1() # "" "" ""
        self.layout.addWidget(self.pgcustom)
        self.layout.addWidget(self.pgcustom1)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())