def showBOX(self): 
    QMessageBox.information(self, "hello", "hello there " + self.nameEdit.text()) 
    print("hello world")
    plt=self.MainGraph 
    #z.plot(x = [0, 1, 2, 4,7,8,9,0], y = [4, 5, 9, 6,1,2,3,4]) 
    import numpy as np 
    import pyqtgraph as pg 

    bufferSize = 1000 
    self.data = np.zeros(bufferSize) 
    self.curve = plt.plot() 
    self.curve.setData() 
    self.line = plt.addLine(x=0) 
    plt.setRange(xRange=[0, bufferSize], yRange=[-50, 50]) 
    self.i = 0 

    def update(): 
      n = 10 # update 10 samples per iteration 
      rand = np.random.normal(size=n) 
      self.data[self.i:self.i+n] = np.clip(self.data[self.i-1] + rand, -50, 50) 
      self.curve.setData(self.data) 
      self.i = (self.i+n) % bufferSize 
      self.line.setValue(self.i) 
    self.update = update 
    self.timer = pg.QtCore.QTimer() 
    self.timer.timeout.connect(self.update) 
    self.timer.start(20) 