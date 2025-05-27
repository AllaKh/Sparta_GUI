import numpy as np
import sys
sys.path.insert(0, r'C:/WinPython/settings')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.magic()

    def magic(self,n):
        n = int(n)
        if n < 3:
            raise ValueError("Size must be at least 3")
        if n % 2 == 1:
            p = np.arange(1, n+1)
            return n*np.mod(p[:, None] + p - (n+3)//2, n) + np.mod(p[:, None] + 2*p-2, n) + 1
        elif n % 4 == 0:
            J = np.mod(np.arange(1, n+1), 4) // 2
            K = J[:, None] == J
            M = np.arange(1, n*n+1, n)[:, None] + np.arange(n)
            M[K] = n*n + 1 - M[K]
        else:
            p = n//2
            M = magic(p)
            M = np.block([[M, M+2*p*p], [M+3*p*p, M+p*p]])
            i = np.arange(p)
            k = (n-2)//4
            j = np.concatenate((np.arange(k), np.arange(n-k+1, n)))
            M[np.ix_(np.concatenate((i, i+p)), j)] = M[np.ix_(np.concatenate((i+p, i)), j)]
            M[np.ix_([k, k+p], [0, k])] = M[np.ix_([k+p, k], [0, k])]
        return M
    
    x = np.arange(0,10)
    mm=magic(self,10)
    y = np.sin(x)
    z=np.random.rand(10,3)  
    plt.plot(x, y)
    plt.plot(x, z)

    plt.show()