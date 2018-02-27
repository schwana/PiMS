import time
import sys
import pyqtgraph as pg
import numpy as np
import os
import socket
import struct


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
      #self.showMaximized()
      #self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

      #Initialise Clock
 #     self.timer = QtCore.QTimer(self)
  #    self.timer.timeout.connect(self.Time)
   #   self.timer.start(1000)

      self.tester = QtCore.QTimer(self)
      self.tester.timeout.connect(self.Test)
      self.tester.start()

    

    def Test(self):
        CurTime=time.time()
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('192.168.0.3', 818)) 

        print (s.recv(1024))
        s.send('Admin\r')
        print(s.recv(1024))
        time.sleep(0.1)
        s.send('admin\r')
        print(s.recv(1024))
        time.sleep(0.5)

        s.send('IN0\r')
        print(s.recv(1024))

        time.sleep(1)


        s.send('ID?\r')
        time.sleep(0.5)
        ID=s.recv(1024)

        print(ID)
                                    
        ID1='SRSRGA100VER0.24SN18402'
        
        time.sleep(1)

        if ID1 in ID:

            print('Successful log in')
            
            self.resize(600,600)
            view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
            #view = pg.ScatterPlotItem()  ## GraphicsView with GraphicsLayout inserted by default
            self.setCentralWidget(view)

            w1 = view.addPlot()
            w1.setLogMode(x=False, y=True)
            #w1.setLabel('left',"Signal", units='A')
            #w1.setLabel('bottom',"Time", units='s')
            #w1.showGrid(x=False, y=True)
            
    ##        x =1
    ##      
    ##        n = 1
    ##        s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 255, 120))
    ##        pos = np.random.normal(size=(2,n), scale=1e-5)
    ##        
    ##        print pos
    ##        spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
    ##
    ##        s1.addPoints(spots)
    ##        w1.addItem(s1)
    ##        
            #Commands to perform a measurement
            s.send('HV*\r')
            print('HV0')
            s.send('NF0\r')
            print('NF0')
            time.sleep(0.5)
            s.send('CA\r')
            print('CA')
            time.sleep(0.5)
            s.send('IN0\r')
            time.sleep(1)
            print(s.recv(1024))

            s.send('MR40 \r')
            time.sleep(5)
            hex_string = s.recv(1024)

            


            n=1
            time.sleep(1)
            j=0
            for x in range(0, 3):
                uf=0.0
                
                MeasureTime40=time.time()
                s.send('MR40 \r')
                time.sleep(5)
                hex_string = s.recv(1024)
                print(repr(hex_string))
                if len(hex_string)==4:
                    u=struct.unpack('<i',hex_string)[0]
                    uf=u*1e-16
                    print('MR40 :', uf)
                else:
                    print('Error Mass 40: ',len(hex_string))
                    uf=0.0
                MeasureTime5=time.time()    
                s.send('MR5\r')
                hex_stringM5 = s.recv(4)
                if len(hex_stringM5)==4:
                    u5=struct.unpack('<i',hex_stringM5)[0]
                    uf5=u5*1e-16
                    print('MR5 :', uf5)
                else:
                    print('Error Mass 5: ',len(hex_stringM5))
                    uf5=0.0
 
                    
                time.sleep(0.5)

                



                #os.system("python /home/pi/PiMS/DisplaySRS/MeasureM40.py")
                #spots = [{'pos': pos[:,i], 'data': 1} for i in range(n)] + [{'pos': [0,0], 'data': 1}]
                #spots2 = [{'pos2': pos2[:,i], 'data2': 1} for i in range(n)] + [{'pos2': [0,0], 'data2': 1}]
                #pos[0]=j
                
    #            fo = open("/home/pi/PiMS/DisplaySRS/M40.txt", "r")
    #            line = fo.readline()
    #            fo.close()
                
    #            uf=float(line)


                s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 120))
                s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 0, 120))
                pos = np.random.normal(size=(2,n), scale=1e-5)
                pos2 = np.random.normal(size=(2,n), scale=1e-5)

                

                pos[0]=MeasureTime40-CurTime
                pos2[0]=MeasureTime5-CurTime

                if uf>0.0:
                    pos[1]=uf
                    s1.addPoints(x=pos[0],y=pos[1])
                    w1.addItem(s1)
                    
                if uf5>0.0:
                    pos2[1]=uf5
                    #s2.addPoints(x=pos2[0],y=pos2[1])
                    #w1.addItem(s2)
                    
                
                #w1.setYRange(-15,-9, padding=0)
                j=j+1
                print("Step %d" % (j))
              
                QtGui.qApp.processEvents()

        s.send('MR0\r')
        print('MR0')

        s.close() 
        sys.exit()
            
        
        
    
    

if __name__ == "__main__":
  app  = QtGui.QApplication(sys.argv)
  myapp = SRSForm()
  app.setStyle('cleanlooks')
  myapp.show()
  sys.exit(app.exec_())
