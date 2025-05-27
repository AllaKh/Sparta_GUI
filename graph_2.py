from PyQt5 import QtCore, QtGui
import pyqtgraph as pg
import random

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginWidget(self)
        self.login_widget.button.clicked.connect(self.plotter)
        self.central_widget.addWidget(self.login_widget)

    def plotter(self):
        self.data =[0]
        self.curve = self.login_widget.plot.getPlotItem().plot()

        self.timer = QtCore.QTimer()
        
        self.timer.timeout.connect(self.updater)
        self.timer.start(10)

    def updater(self):

        self.data.append(self.data[-1]+0.2*(0.5-random.random()) )
        self.curve.setData(self.data)


class LoginWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.button = QtGui.QPushButton('Start Plotting')
        layout.addWidget(self.button)
        self.plot = pg.PlotWidget()
        self.plot2 = pg.PlotWidget()
        layout.addWidget(self.plot)
        layout.addWidget(self.plot2)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()