import time
import sys
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
      self.timer = QtCore.QTimer(self)
      self.timer.timeout.connect(self.Time)
      self.timer.start(1000)

      self.tester = QtCore.QTimer(self)
      self.tester.timeout.connect(self.Test)
      self.tester.start()

    def Time(self):
        self.ui.lcdTime.display(strftime("%H"+":"+"%M"+":"+"%S"))

    def Test(self):
        for x in range(0, 20):
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
