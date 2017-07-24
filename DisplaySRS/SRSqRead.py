import time
import sys
import pyqtgraph as pg
import numpy as np

from time import strftime

from PyQt4 import QtCore, QtGui

from displaysrs import Ui_displaySRS

print "SRSqRead.py running"

class SRSForm(QtGui.QMainWindow):


    def __init__(self, parent=None):
      QtGui.QWidget.__init__(self, parent)
      #QtCore.QThread.__init__(self, parent)
      self.ui = Ui_displaySRS()
      self.ui.setupUi(self)
      self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

      #Initialise Clock
 #     self.timer = QtCore.QTimer(self)
  #    self.timer.timeout.connect(self.Time)
   #   self.timer.start(1000)

      self.tester = QtCore.QTimer(self)
      self.tester.timeout.connect(self.Test)
      self.tester.start()
      
      self.resize(800,800)
      view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
      self.setCentralWidget(view)


      w1 = view.addPlot()

      
      n = 100
      s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
      pos = np.random.normal(size=(2,n), scale=1e-5)
      spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
      s1.addPoints(spots)
      w1.addItem(s1)
        
      


#    def Time(self):
#        self.ui.lcdTime.display(strftime("%H"+":"+"%M"+":"+"%S"))

    def Test(self):

        for x in range(0, 10):
            print("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        sys.exit()
        
        
    
    

if __name__ == "__main__":
  app  = QtGui.QApplication(sys.argv)
  myapp = SRSForm()
  app.setStyle('cleanlooks')
  myapp.show()
  sys.exit(app.exec_())
