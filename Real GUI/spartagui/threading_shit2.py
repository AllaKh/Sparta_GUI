import threading
import time 
from queue import Queue
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

import design

print_lock = threading.Lock()

class App(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # return None

class MyThread(threading.Thread):
    def __init__(self, queue, args=(), kwargs=None):
        threading.Thread.__init__(self, args=(), kwargs=None)
        self.queue_input = queue[1]
        self.daemon = True
        self.receive_messages = args[0]
        self.main_method = args[1]

    def run(self):
        print ("start",threading.currentThread().getName(), self.receive_messages)
        print("queue size before get",self.queue.qsize())
        val = self.queue.get()
        print("queue size after get",self.queue.qsize())

        print("get msg")
        self.do_thing_with_message(val)

    def do_thing_with_message(self, message):
        print("in do_thing_with_message",self.receive_messages)
        if self.receive_messages==1:
            self.main_method()
        if self.receive_messages:
            print("self.receive_messages")
            time.sleep(0.5)

            with print_lock:
                print (threading.currentThread().getName(), "Received {}".format(message))
        print("bye")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()

if __name__ == '__main__':
    threads = []
    for t in range(10):
        q_input = Queue()
        q_out = Queue()
        q_tuple = (q_input,q_out,...mn..)
        threads.append(MyThread(q, args=(t+1,main)))
        threads[t].start()
        time.sleep(0.1)
    counter=0
    for t in threads:
        counter=counter+1
        print("ilia",counter)
        # print("queue size before put",qsize(q))

        t.queue.put('Print this! %d' %counter)
        print("queue size after put",q.empty())

        time.sleep(0.1)

    for t in threads:
        t.join()