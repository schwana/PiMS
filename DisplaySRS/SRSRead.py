import time
import sys
import pyqtgraph as pg
import numpy as np
import os
import socket
import struct
import math


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
      Connect_Status = False

      
      #Initialise Clock
      self.tester = QtCore.QTimer(self)
      self.tester.timeout.connect(self.AttemptReadQMA)
      self.tester.start()

    def AttemptReadQMA(self):
        try:
            print "Connecting to QMA"
            self.RGAConnect()
            print "self.test finished"
        except socket.error, exc:
            print "Caught exception socket.error : %s" % exc
            self.OfflineMode()
            
    def OfflineMode(self):

        print "Offline Mode - using dummy file:"

        HomeDir=os.getenv("HOME")
        WorkDir=HomeDir+'/PiMS/DisplaySRS/HeDummy.csv'
        print(WorkDir)

        my_data=np.genfromtxt(WorkDir,delimiter=',')

        CurTime=time.time()

        self.resize(600,600)
        #win = pg.PlotWidget()
        win = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
        self.setCentralWidget(win)

        w1 = win.addPlot()
        #w1.setLogMode(x=False, y=True)
        w1.setLabel('left',"log(Signal)")
        #w1.setLabel('bottom',"Time", units='s')
        w1.showGrid(x=False, y=True)
        
        #w1.setYRange(-1,2, padding=0)

        s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 255), name='H')
        s2 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 0, 255), name='3He')
        s3 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 255, 255),name='4He')
        s4 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 0, 255), name='40Ar')
        s5 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 255, 255), name='BL')

        w1.addItem(s1)
        w1.addItem(s2)
        w1.addItem(s3)
        w1.addItem(s4)
        w1.addItem(s5)
       
        #s1.enableAutoSIPrefix(enable=False)

        spots1=[]
        spots3=[]
        spots4=[]
        spots5=[]
        spots40=[]

        outputM1=[]
        outputM1t=[]
        outputM3=[]
        outputM3t=[]
        outputM4=[]
        outputM4t=[]
        outputM5=[]
        outputM5t=[]
        outputM40=[]
        outputM40t=[]

        stepTime=0.5

        for x in range (0,len(my_data)):
            #Split the line into masses
            dataLine=my_data[x]
            time.sleep(stepTime)
            
            #### READ MASS 1  ####
            MeasureTimeM1=time.time()
            uf_m1 = float(dataLine[0])
            x1=MeasureTimeM1-CurTime
            y1=math.log10(uf_m1)
            spots1.append({'pos':(x1,y1)})
            s1.addPoints(spots1)
            QtGui.qApp.processEvents()
            outputM1.append(uf_m1)
            outputM1t.append(MeasureTimeM1)
            time.sleep(stepTime)
            #### READ MASS 3  ####
            uf_m3 = float(dataLine[1])
            MeasureTimeM3=time.time()
            x3=MeasureTimeM3-CurTime
            y3=math.log10(uf_m3)
            spots3.append({'pos':(x3,y3)})
            s2.addPoints(spots3)
            QtGui.qApp.processEvents()
            outputM3.append(uf_m3)
            outputM3t.append(MeasureTimeM3)
            time.sleep(stepTime)
            #### READ MASS 4  ####
            uf_m4 = float(dataLine[2])
            MeasureTimeM4=time.time()
            x4=MeasureTimeM4-CurTime
            y4=math.log10(uf_m4)
            spots4.append({'pos':(x4,y4)})
            s3.addPoints(spots4)
            QtGui.qApp.processEvents()
            outputM4.append(uf_m4)
            outputM4t.append(MeasureTimeM4)
            time.sleep(stepTime)
            #### READ MASS 5  ####
            uf_m5 = float(dataLine[3])
            MeasureTimeM5=time.time()
            x5=MeasureTimeM5-CurTime
            y5=math.log10(uf_m5)
            spots5.append({'pos':(x5,y5)})
            s4.addPoints(spots5)
            QtGui.qApp.processEvents()
            outputM5.append(uf_m5)
            outputM5t.append(MeasureTimeM5)
            time.sleep(stepTime)
            #### READ MASS 40  ####
            uf_m40 = float(dataLine[4])
            MeasureTimeM40=time.time()
            x40=MeasureTimeM40-CurTime
            y40=math.log10(uf_m40)
            spots40.append({'pos':(x40,y40)})
            s5.addPoints(spots40)
            QtGui.qApp.processEvents()
            outputM40.append(uf_m40)
            outputM40t.append(MeasureTimeM40)
            time.sleep(stepTime)

        print("Scan Complete")

        #Output to file
        self.outputData(outputM1, outputM1t,
                        outputM3, outputM3t,
                        outputM4, outputM4t,
                        outputM5, outputM5t,
                        outputM40, outputM40t)
        
        print len(outputM1)
        sys.exit()
      

    def RGAConnect(self):
        CurTime=time.time()
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(20) #20 second timeout
        #s.settimeout(1) #1 second timeout

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
            w1.setLabel('left',"log(Signal)")
            w1.showGrid(x=False, y=True)
            
            s1 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 0, 0, 255), name='H')
            s3 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 0, 255), name='3He')
            s4 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(0, 0, 255, 255),name='4He')
            s5 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(255, 255, 0, 255), name='40Ar')
            s40 = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(0, 255, 255, 255), name='BL')

            w1.addItem(s1)
            w1.addItem(s3)
            w1.addItem(s4)
            w1.addItem(s5)
            w1.addItem(s40)
           
            spots1=[]
            spots3=[]
            spots4=[]
            spots5=[]
            spots40=[]
                
            #Commands to perform a measurement
            s.send('HV1000\r')
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

            outputM1=[]
            outputM1t=[]
            outputM3=[]
            outputM3t=[]
            outputM4=[]
            outputM4t=[]
            outputM5=[]
            outputM5t=[]
            outputM40=[]
            outputM40t=[]


            n=1
            time.sleep(1)
            j=0
            for x in range(0, 20):
   
            #### READ MASS 1  ####
                MeasureTimeM1=time.time()
                s.send('MR1 \r')
                time.sleep(5)
                hex_string = s.recv(1024)
                x1=MeasureTimeM1-CurTime
                if len(hex_string)==4:
                    u1=struct.unpack('<i',hex_string)[0]
                    uf_m1=u1*1e-16
                    outputM1.append(uf_m1)
                    outputM1t.append(MeasureTimeM1)
                    print('MR1 :', uf_m1)
                    if uf_m1>0:
                        y1=math.log10(uf_m1)
                        spots1.append({'pos':(x1,y1)})
                        s1.addPoints(spots1)
                        QtGui.qApp.processEvents()
                else:
                    print('Error Mass 1: ',len(hex_string))
                s.send('IN0\r')
                time.sleep(1)
                print(s.recv(1024))               

            #### READ MASS 3  ####
                MeasureTimeM3=time.time()
                s.send('MR3 \r')
                time.sleep(5)
                hex_string = s.recv(1024)
                x3=MeasureTimeM3-CurTime
                if len(hex_string)==4:
                    u3=struct.unpack('<i',hex_string)[0]
                    uf_m3=u3*1e-16
                    outputM3.append(uf_m3)
                    outputM3t.append(MeasureTimeM3)
                    print('MR3 :', uf_m3)
                    if uf_m3>0:
                        y3=math.log10(uf_m3)
                        spots3.append({'pos':(x3,y3)})
                        s3.addPoints(spots3)
                        QtGui.qApp.processEvents()
                else:
                    print('Error Mass 3: ',len(hex_string))

                s.send('IN0\r')
                time.sleep(1)
                print(s.recv(1024))  

            #### READ MASS 4  ####
                MeasureTimeM4=time.time()
                s.send('MR4 \r')
                time.sleep(5)
                hex_string = s.recv(1024)
                x4=MeasureTimeM4-CurTime
                if len(hex_string)==4:
                    u4=struct.unpack('<i',hex_string)[0]
                    uf_m4=u4*1e-16
                    outputM4.append(uf_m4)
                    outputM4t.append(MeasureTimeM4)
                    print('MR4 :', uf_m4)
                    if uf_m4>0:
                        y4=math.log10(uf_m4)
                        spots4.append({'pos':(x4,y4)})
                        s4.addPoints(spots4)
                        QtGui.qApp.processEvents()
                else:
                    print('Error Mass 4: ',len(hex_string))
                s.send('IN0\r')
                time.sleep(1)
                print(s.recv(1024))  


            #### READ MASS 5  ####
                MeasureTimeM5=time.time()
                s.send('MR5 \r')
                time.sleep(5)
                hex_string = s.recv(1024)
                x5=MeasureTimeM5-CurTime
                if len(hex_string)==4:
                    u5=struct.unpack('<i',hex_string)[0]
                    uf_m5=u5*1e-16
                    outputM5.append(uf_m5)
                    outputM5t.append(MeasureTimeM5)
                    print('MR5 :', uf_m5)
                    if uf_m5>0:
                        y5=math.log10(uf_m5)
                        spots5.append({'pos':(x5,y5)})
                        s5.addPoints(spots5)
                        QtGui.qApp.processEvents()
                else:
                    print('Error Mass 5: ',len(hex_string))
                    
                s.send('IN0\r')
                time.sleep(1)
                print(s.recv(1024))
            
            #### READ MASS 40  ####
                MeasureTimeM40=time.time()
                s.send('MR40 \r')
                time.sleep(5)
                hex_string = s.recv(1024)
                x40=MeasureTimeM40-CurTime
                if len(hex_string)==4:
                    u40=struct.unpack('<i',hex_string)[0]
                    uf_m40=u40*1e-16
                    print('MR40 :', uf_m40)
                    if uf_m40>0:
                        outputM40.append(uf_m40)
                        outputM40t.append(MeasureTimeM40)                        
                        y40=math.log10(uf_m40)
                        spots40.append({'pos':(x40,y40)})
                        s40.addPoints(spots40)
                        QtGui.qApp.processEvents()
                else:
                    print('Error Mass 40: ',len(hex_string))
 
                time.sleep(0.5)

                j=j+1
                print("Step %d" % (j))
              
                QtGui.qApp.processEvents()
                
                s.send('IN0\r')
                time.sleep(1)
                print(s.recv(1024))

            
        s.send('MR0\r')
        print('MR0')

        print("FINISHED - Output to file")

        #Output to file
        self.outputData(outputM1, outputM1t,
                        outputM3, outputM3t,
                        outputM4, outputM4t,
                        outputM5, outputM5t,
                        outputM40, outputM40t)

        s.close() 
        sys.exit()
        
    def outputData(self, M1,M1t,M3,M3t,M4,M4t,M5,M5t,M40,M40t):
        print("Output Data to File")

        _USERNAME = os.getenv("SUDO_USER") or os.getenv("USER")
        _HOME = os.path.expanduser('~'+_USERNAME)

        HNum = _HOME+'/PiMS/Hnum.txt'

        #Get current helium run number
        fo = open(HNum, "r")
        HeNum = fo.readline()
        fo.close() 

        FileName = 'He'+HeNum+'.txt'

        WorkDir= _HOME+'/Results/'+FileName

        #Read Inlet Line

        foRun = open(WorkDir,"r")
        lines = foRun.readlines()

        inletLine = lines[1].split(",")
        inletTime=float(inletLine[1])
                
        foRun.close()
        #Recalculate inlet times to give absolute values
        for x in range (0, len(M1)):
            M1t[x]=float(str(M1t[x]))-inletTime
            M3t[x]=float(str(M3t[x]))-inletTime
            M4t[x]=float(str(M4t[x]))-inletTime
            M5t[x]=float(str(M5t[x]))-inletTime
            M40t[x]=float(str(M40t[x]))-inletTime


        #Re-open file to append times, currents
        foRun = open(WorkDir,"a")

        #Collected data
        for x in range (0, len(M1)):

            outputString=(str(M1t[x])+","+str(M1[x])+","+
                          str(M3t[x])+","+str(M3[x])+","+
                          str(M4t[x])+","+str(M4[x])+","+
                          str(M5t[x])+","+str(M5[x])+","+
                          str(M40t[x])+","+str(M40[x]))
            
            foRun.write(outputString+'\n')

        foRun.close()
        
        
        
    

if __name__ == "__main__":
  app  = QtGui.QApplication(sys.argv)
  myapp = SRSForm()
  app.setStyle('cleanlooks')
  myapp.show()
  sys.exit(app.exec_())
