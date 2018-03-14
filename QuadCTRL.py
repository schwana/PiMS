import sys
import time
import os
import serial

from PyQt4 import QtCore, QtGui
from time import strftime


from QuadCTRL_ui import Ui_QuadCTRL


#To avoid issues when running code on anything
#other than a Pi, use try ... except. 

try:
    import RPi.GPIO as GPIO
    print ("RPi.GPIO Imported")
except RuntimeError:
    print("Error importing RPi.GPIO!")


class MyForm(QtGui.QMainWindow):


    def __init__(self, parent=None):
      QtGui.QWidget.__init__(self, parent)
      self.ui = Ui_QuadCTRL()
      self.ui.setupUi(self)
      #Comment next line for frame
#      self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
      self.showMaximized()
      #Initialise Clock
      self.timer = QtCore.QTimer(self)
      self.timer.timeout.connect(self.Time)
      self.timer.start(1000)
      #Initialise Temperature Updater
      self.timer1 = QtCore.QTimer(self)
      self.timer1.timeout.connect(self.UpdateTemperature)
      self.timer1.start(10000)
      #Update Tank Numbers (shot numbers)
      self.UpdateTankNumbers()
      #Initialise the valves
      self.InitValves()
      #Initialise the various buttons
      self.InitButtons()
      self.disableValveButtons()
      self.disableGetter()

## -------------- INITIALISATION ----------------##


    def InitButtons(self):
        #Getter Dial
      QtCore.QObject.connect(self.ui.dialGetter,QtCore.SIGNAL("valueChanged(int)"),self.dialGetterChange)
        #LineBlank Button
      QtCore.QObject.connect(self.ui.lbButton,QtCore.SIGNAL("clicked()"),self.LineBlank)
      self.ui.lbButton.setStyleSheet("background-color: green") 
        #Standard Button
      QtCore.QObject.connect(self.ui.stdButton,QtCore.SIGNAL("clicked()"),self.QShot)
      self.ui.stdButton.setStyleSheet("background-color: green")
       #Sample Button
      QtCore.QObject.connect(self.ui.sampleButton,QtCore.SIGNAL("clicked()"),self.LineBlank)
      self.ui.sampleButton.setStyleSheet("background-color: green")
       #Running Button (doesn't do anything)
      QtCore.QObject.connect(self.ui.runningButton,QtCore.SIGNAL("clicked()"),self.runningPushed)
      self.ui.runningButton.setStyleSheet("background-color: green")
       #Auto/manual Button 
      QtCore.QObject.connect(self.ui.pushButtonAuto,QtCore.SIGNAL("clicked()"),self.AutoPushed)
      self.ui.pushButtonAuto.setStyleSheet("background-color: orange")
       #Auto/manual Button 
      QtCore.QObject.connect(self.ui.runAllButton,QtCore.SIGNAL("clicked()"),self.RunAllSamples)
      self.ui.runAllButton.setStyleSheet("background-color: green")
      #Test Check Box
      QtCore.QObject.connect(self.ui.checkBoxTest,QtCore.SIGNAL("stateChanged(int)"),self.TestBox)
      self.TestBox()
##       #Hole + Button 
##      QtCore.QObject.connect(self.ui.pushButtonHolePlus,QtCore.SIGNAL("clicked()"),self.HolePlus)
##       #Hole - Button 
##      QtCore.QObject.connect(self.ui.pushButtonHoleMinus,QtCore.SIGNAL("clicked()"),self.HoleMinus)
      #Table (Sample)
      QtCore.QObject.connect(self.ui.tableWidgetSamples,QtCore.SIGNAL("cellClicked(int,int)"),self.SampleTable)
      QtCore.QObject.connect(self.ui.tableWidgetStandards1,QtCore.SIGNAL("cellClicked(int,int)"),self.StdTable1)
      QtCore.QObject.connect(self.ui.tableWidgetStandards2,QtCore.SIGNAL("cellClicked(int,int)"),self.StdTable2)
      #QtCore.QObject.connect(self.ui.tableWidgetSamples,QtCore.SIGNAL("cellChanged(int,int)"),self.SampleTable)
      #QtCore.QObject.connect(self.ui.tableWidgetStandards1,QtCore.SIGNAL("cellChanged(int,int)"),self.StdTable1)
      #QtCore.QObject.connect(self.ui.tableWidgetStandards2,QtCore.SIGNAL("cellChanged(int,int)"),self.StdTable2)
      
      


    def SampleTable(self):

        #on clicking any cell, loop through the cells and leave any cells which are empty white.
        #colour purple any populated cells.
        for i in range (0,self.ui.tableWidgetSamples.rowCount()):
            for j in range (0,self.ui.tableWidgetSamples.columnCount()):
                cellText=self.ui.tableWidgetSamples.item(i,j)
                if cellText is None:
                    try:
                        self.ui.tableWidgetSamples.item(i,j).setBackground(QtGui.QColor(255,255,255))
                    except:
                        pass
                else:
                    print (cellText.text())
                    if  cellText.text().replace(" ","")=="":
                        self.ui.tableWidgetSamples.item(i,j).setBackground(QtGui.QColor(255,255,255))
                        self.ui.tableWidgetSamples.item(i,j).setForeground(QtGui.QColor(0,0,0))
                    else:    
                        self.ui.tableWidgetSamples.item(i,j).setBackground(QtGui.QColor(100,100,150))
                        self.ui.tableWidgetSamples.item(i,j).setForeground(QtGui.QColor(255,255,255))
       

    def StdTable1(self):

        #on clicking any cell, loop through the cells and leave any cells which are empty white.
        #colour purple any populated cells.
        for i in range (0,self.ui.tableWidgetStandards1.rowCount()):
            for j in range (0,self.ui.tableWidgetStandards1.columnCount()):
                cellText=self.ui.tableWidgetStandards1.item(i,j)
                if cellText is None:
                    try:
                        self.ui.tableWidgetStandards1.item(i,j).setBackground(QtGui.QColor(255,255,255))
                    except:
                        pass
                else:
                    if  cellText.text().replace(" ","")=="":
                        self.ui.tableWidgetStandards1.item(i,j).setBackground(QtGui.QColor(255,255,255))
                        self.ui.tableWidgetStandards1.item(i,j).setForeground(QtGui.QColor(0,0,0))
                    else:    
                        self.ui.tableWidgetStandards1.item(i,j).setBackground(QtGui.QColor(100,100,150))
                        self.ui.tableWidgetStandards1.item(i,j).setForeground(QtGui.QColor(255,255,255))
                        #self.ui.tableWidgetStandards1.clear()

 
 
                
    def StdTable2(self):

        #on clicking any cell, loop through the cells and leave any cells which are empty white.
        #colour purple any populated cells.
        for i in range (0,self.ui.tableWidgetStandards2.rowCount()):
            for j in range (0,self.ui.tableWidgetStandards2.columnCount()):
                cellText=self.ui.tableWidgetStandards2.item(i,j)
                if cellText is None:
                    try:
                        self.ui.tableWidgetStandards2.item(i,j).setBackground(QtGui.QColor(255,255,255))
                    except:
                        pass
                else:
                    if  cellText.text().replace(" ","")=="":
                        self.ui.tableWidgetStandards2.item(i,j).setBackground(QtGui.QColor(255,255,255))
                        self.ui.tableWidgetStandards2.item(i,j).setForeground(QtGui.QColor(0,0,0))
                    else:    
                        self.ui.tableWidgetStandards2.item(i,j).setBackground(QtGui.QColor(100,100,150))
                        self.ui.tableWidgetStandards2.item(i,j).setForeground(QtGui.QColor(255,255,255))
      




        
    def AutoPushed(self):
        #CHANGE THIS SO THAT PRESSING THE BUTTON ENABLES/DISABLES THE VALVE BUTTONS
	#HAVE A SEPARATE THREAD TO DISABLE THE BUTTONS - VALVES AS PART OF ONE
	#BUTTON GROUP? WILL SAVE CODE LATER.... LOOK UP BUTTON GROUPS
        if self.ui.pushButtonAuto.isChecked():
            self.enableValveButtons()
            self.enableGetter()
            self.ui.pushButtonAuto.setStyleSheet("background-color: green")
            self.ui.pushButtonAuto.setText("Manual")
        else:
            self.disableValveButtons()
            self.disableGetter()
            self.ui.pushButtonAuto.setStyleSheet("background-color: orange")
            self.ui.pushButtonAuto.setText("Auto")
            

    def TestBox(self):
        if self.ui.checkBoxTest.isChecked():
            print "In Test Mode"
        else:
            print "In GPIO Mode"
            self.GPIOSetup()

    def InitValves(self):
              #Setup Valves (initially all OFF)     
        #Valve 1 - Q pipette (tank)
      QtCore.QObject.connect(self.ui.v1,QtCore.SIGNAL("clicked()"),self.btn1Push)
      self.ui.v1.setStyleSheet("background-color: orange")
        #Valve 2 - Q pipette (line)
      QtCore.QObject.connect(self.ui.v2,QtCore.SIGNAL("clicked()"),self.btn2Push)
      self.ui.v2.setStyleSheet("background-color: orange")
        #Valve 3 - Spike pipette (line)
      QtCore.QObject.connect(self.ui.v3,QtCore.SIGNAL("clicked()"),self.btn3Push)
      self.ui.v3.setStyleSheet("background-color: orange")
        #Valve 4 - Spike pipette (tank)
      QtCore.QObject.connect(self.ui.v4,QtCore.SIGNAL("clicked()"),self.btn4Push)
      self.ui.v4.setStyleSheet("background-color: orange")
        #Valve 6 - Ion Pump
      QtCore.QObject.connect(self.ui.v6,QtCore.SIGNAL("clicked()"),self.btn6Push)
      self.ui.v6.setStyleSheet("background-color: orange")
        #Valve 7 - Quad
      QtCore.QObject.connect(self.ui.v7,QtCore.SIGNAL("clicked()"),self.btn7Push)
      self.ui.v7.setStyleSheet("background-color: orange")
        #Valve 8 - Volume A
      QtCore.QObject.connect(self.ui.v8,QtCore.SIGNAL("clicked()"),self.btn8Push)
      self.ui.v8.setStyleSheet("background-color: orange")
        #Valve 10 - Laser Port
      QtCore.QObject.connect(self.ui.v10,QtCore.SIGNAL("clicked()"),self.btn10Push)
      self.ui.v10.setStyleSheet("background-color: orange")
        #Valve 11 - Hot Getter
      QtCore.QObject.connect(self.ui.v11,QtCore.SIGNAL("clicked()"),self.btn11Push)
      self.ui.v11.setStyleSheet("background-color: orange")
        #Valve 12 - Backing Pump
      QtCore.QObject.connect(self.ui.v12,QtCore.SIGNAL("clicked()"),self.btn12Push)
      self.ui.v12.setStyleSheet("background-color: orange")
        #Valve 13 - Turbo Pump
      QtCore.QObject.connect(self.ui.v13,QtCore.SIGNAL("clicked()"),self.btn13Push)
      self.ui.v13.setStyleSheet("background-color: orange")

    def UpdateTankNumbers(self):
        fo = open("Qnum.txt", "rw+")
        line = fo.readline()
        self.ui.lblQnum.setText(line)
        fo.close()

        fo = open("Hnum.txt", "rw+")
        line = fo.readline()
        self.ui.lblHnum.setText(line)
        fo.close()        

    def Time(self):
        self.ui.lcdTime.display(strftime("%H"+":"+"%M"+":"+"%S"))
   #     self.UpdateTemperature()
        

    def UpdateTemperature(self):
        fo = open("Temperature.txt", "r")
        line = fo.readline()
        degreeChar = u'\N{DEGREE SIGN}'
  #      print line
        self.ui.labelTemperature.setText("{:.1f}".format(float(line))+degreeChar+"C")
        fo.close()

## -------------- VALVE OPERATIONS ----------------##

    def disableValveButtons(self):
        self.ui.v1.setEnabled(False)
        self.ui.v2.setEnabled(False)
        self.ui.v3.setEnabled(False)
        self.ui.v4.setEnabled(False)
        self.ui.v6.setEnabled(False)
        self.ui.v7.setEnabled(False)
        self.ui.v8.setEnabled(False)
        self.ui.v10.setEnabled(False)
        self.ui.v11.setEnabled(False)
        self.ui.v12.setEnabled(False)
        self.ui.v13.setEnabled(False)

    def disableGetter(self):
        self.ui.dialGetter.setEnabled(False)
        
    def enableGetter(self):
        self.ui.dialGetter.setEnabled(True)

    def enableValveButtons(self):
        self.ui.v1.setEnabled(True)
        self.ui.v2.setEnabled(True)
        self.ui.v3.setEnabled(True)
        self.ui.v4.setEnabled(True)
        self.ui.v6.setEnabled(True)
        self.ui.v7.setEnabled(True)
        self.ui.v8.setEnabled(True)
        self.ui.v10.setEnabled(True)
        self.ui.v11.setEnabled(True)
        self.ui.v12.setEnabled(True)
        self.ui.v13.setEnabled(True)


    def btn1Push(self):
        #check if v2 is open
        if self.ui.v2.isChecked():
         self.ui.v1.setChecked(False)
        else:
         if self.ui.v1.isChecked():
             self.v1open()
         else:
            self.v1close()

    def btn2Push(self):
        if self.ui.v1.isChecked():
         self.ui.v2.setChecked(False)
        else:
            if self.ui.v2.isChecked():
               self.v2open()
            else:
               self.v2close()
               
    def btn3Push(self):
        #check if v4 is open
        if self.ui.v4.isChecked():
         self.ui.v3.setChecked(False)
        else:
         if self.ui.v3.isChecked():
            self.v3open()
         else:
            self.v3close()


    def btn4Push(self):
        #check if v3 is open
        if self.ui.v3.isChecked():
         self.ui.v4.setChecked(False)
        else:
         if self.ui.v4.isChecked():
            self.v4open()
         else:
            self.v4close()

    def btn6Push(self):
       if self.ui.v6.isChecked():
          self.v6open()
       else:
          self.v6close()
        
    def btn7Push(self):
       if self.ui.v7.isChecked():
          self.v7open()
       else:
          self.v7close()

    def btn8Push(self):
       if self.ui.v8.isChecked():
          self.v8open()
       else:
          self.v8close()

    def btn10Push(self):
       if self.ui.v10.isChecked():        
          self.v10open()
       else:
          self.v10close()

    def btn11Push(self):
       if self.ui.v11.isChecked():
          self.v11open()
       else:
          self.v11close()
            
    def btn12Push(self):
       if self.ui.v12.isChecked():
          self.v12open()
       else:
          self.v12close()

    def btn13Push(self):
       if self.ui.v13.isChecked():
          self.v13open()
       else:
          self.v13close()

    def dialGetterChange(self):
       value = self.ui.dialGetter.value()
       self.ui.getterLabel.setText(str(value)+" minutes")
       

    def v1open(self):
        #Open Valve 1
        self.ui.v1.setStyleSheet("background-color: green")
        self.ui.progressLabel.setText("v1 open")
        QtGui.qApp.processEvents()
        if self.ui.runningButton.isChecked():
            pass
        else:    
            self.He4Increment()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(4,GPIO.HIGH)
            


    def v1close(self):
        #Close Valve 1:
        self.ui.progressLabel.setText("v1 closed")
        self.ui.v1.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(4,GPIO.LOW)

    def v2open(self):
        #Open Valve 2
        self.ui.progressLabel.setText("v2 open")
        self.ui.v2.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(17,GPIO.HIGH)

    def v2close(self):
        #Close Valve 2:
        self.ui.progressLabel.setText("v2 closed")
        self.ui.v2.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(17,GPIO.LOW)

    def v3open(self):
        #Open Valve 3
        self.ui.progressLabel.setText("v3 open")
        self.ui.v3.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(27,GPIO.HIGH)

    def v3close(self):
        #Close Valve 3:
        self.ui.progressLabel.setText("v3 closed")
        self.ui.v3.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(27,GPIO.LOW)
        

    def v4open(self):
        #Open Valve 4
        self.ui.progressLabel.setText("v4 open")
        self.ui.v4.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        if self.ui.runningButton.isChecked():
            pass
        else:    
            self.He3Increment()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(22,GPIO.HIGH)
        

    def v4close(self):
        #Close Valve 4:
        self.ui.progressLabel.setText("v4 closed")
        self.ui.v4.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(22,GPIO.LOW)
        

    def v5open(self):  #CURRENTLY NOT USED
        #Open Valve 5
        self.ui.progressLabel.setText("v5 open")
        self.ui.v5.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(5,GPIO.HIGH)
        

    def v5close(self): #CURRENTLY NOT USED
        #Close Valve 5:
        self.ui.progressLabel.setText("v5 closed")
        self.ui.v5.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(5,GPIO.LOW)
        

    def v6open(self):
        #Open Valve 6
        self.ui.progressLabel.setText("v6 open")
        self.ui.v6.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            print ("TEST POINT - GPIO 6 NOT HIGH")
        else:
            GPIO.output(6,GPIO.HIGH)
            print ("TEST POINT - GPIO 6 HIGH")
        

    def v6close(self):
        #Close Valve 6:
        self.ui.progressLabel.setText("v6 closed")
        self.ui.v6.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(6,GPIO.LOW)
        

    def v7open(self):
        #Open Valve 7
        self.ui.progressLabel.setText("v7 open")
        self.ui.v7.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(13,GPIO.HIGH)
        

    def v7close(self):
        #Close Valve 7:
        self.ui.progressLabel.setText("v7 closed")
        self.ui.v7.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(13,GPIO.LOW)
        

    def v8open(self):
        #Open Valve 8
        self.ui.progressLabel.setText("v8 open")
        self.ui.v8.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(19,GPIO.HIGH)
        

    def v8close(self):
        #Close Valve 8:
        self.ui.progressLabel.setText("v8 closed")
        self.ui.v8.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(19,GPIO.LOW)
        

    def v10open(self):
        #Open Valve 10
        self.ui.progressLabel.setText("v10 open")
        self.ui.v10.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(26,GPIO.HIGH)
        

    def v10close(self):
        #Close Valve 10:
        self.ui.progressLabel.setText("v10 closed")
        self.ui.v10.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(26,GPIO.LOW)
        

    def v11open(self):
        #Open Valve 11
        self.ui.progressLabel.setText("v11 open")
        self.ui.v11.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(18,GPIO.HIGH)
        

    def v11close(self):
        #Close Valve 11:
        self.ui.progressLabel.setText("v11 closed")
        self.ui.v11.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(18,GPIO.LOW)
        

    def v12open(self):
        #Open Valve 12
        self.ui.progressLabel.setText("v12 open")
        self.ui.v12.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(23,GPIO.HIGH)
        

    def v12close(self):
        #Close Valve 12:
        self.ui.progressLabel.setText("v12 closed")
        self.ui.v12.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(23,GPIO.LOW)
        

    def v13open(self):
        #Open Valve 13
        self.ui.progressLabel.setText("v13 open")
        self.ui.v13.setStyleSheet("background-color: green")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(24,GPIO.HIGH)
        

    def v13close(self):
        #Close Valve 13:
        self.ui.progressLabel.setText("v13 closed")
        self.ui.v13.setStyleSheet("background-color: orange")
        QtGui.qApp.processEvents()
        time.sleep(0.5)
        #GPIO signal here
        if self.ui.checkBoxTest.isChecked():
            pass
        else:
            GPIO.output(24,GPIO.LOW)
        

    def runningPushed(self):
        pass
        

## -------------- LB, Q, SAMPLE ----------------##

    def RunPrelim(self):
        #Diable getter dial
        self.ui.dialGetter.setEnabled(False)
        #Disable buttons
        self.ui.pushButtonAuto.setEnabled(False)
        #set valves to default position
        #Close first
        self.v13close()
        self.v1close()
        self.v2close()
        self.v3close()
        self.v4close()
        #Open
        self.v6open()                               
        self.v7open()
        self.v8open()
        self.v10open()
        self.v11open()
        self.v12open()
        #start sequence
        self.ui.lblProcess.setText("Close Laser Port")
        self.v10close()
        #pump pipettess
        self.ui.lblProcess.setText("Pump pipettes")
        self.v2open()
        self.v3open()
        for x in range(0, 5):
            self.ui.progressLabel.setText("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        #close pipettes
        self.v2close()
        self.v3close()
        self.ui.lblProcess.setText("Load pipettes")

    def LoadPipettesSampleBlank(self):
        #load pipettes
        self.v1close()
        self.v4open()
        self.He3Increment()
        for x in range(0, 5):
            self.ui.progressLabel.setText("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        self.v1close()
        self.v4close()

    def LoadPipettesStandard(self):
        #load pipettes
        self.v1open()
        self.He4Increment()
        self.v4open()
        self.He3Increment()
        for x in range(0, 5):
            self.ui.progressLabel.setText("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        self.v1close()
        self.v4close()        



    def PreMeasure(self):
        #Valve operations post pippette load
                #Get Ready to Measure
        self.ui.lblProcess.setText("Close To Vol A")
        #Close v8
        self.v8close()
        #empty pipettes
        self.ui.lblProcess.setText("Release pipettes")
        self.v2open()
        self.v3open()
        #Open laser port
        self.ui.lblProcess.setText("Open Laser Port")
        self.v10open()
        for x in range(0, 5):
            self.ui.progressLabel.setText("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        #close pipettes
        self.ui.lblProcess.setText("Close Pipettes")
        self.v2close()
        self.v3close()
        #wait gettering time
        #Get Getter delay
        value = 60*self.ui.dialGetter.value()

        self.ui.lblProcess.setText("Getter")
        #for x in range(0, value):
        for x in range(0, 10):
            self.ui.progressLabel.setText("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        self.ui.lblProcess.setText("Close Ion Pump")   
        #Close v6
        self.v6close()    


    def QuadMeaure(self):
        #Open v8 - Inlet   
        self.v8open()
        self.ui.lblProcess.setText("Inlet and Measure")
        #wait then start quad
#        for x in range(0, 60):
#            self.ui.progressLabel.setText("Time %d" % (x))
#            time.sleep(1)
        QtGui.qApp.processEvents()

#        self.ui.lblProcess.setText("Start Measurement")
        HomeDir=os.getenv("HOME")
        WorkDir=HomeDir+'/PiMS/DisplaySRS/SRSRead.py'
        print(WorkDir)

        os.system("python "+WorkDir)
        self.ui.lblProcess.setText("End Measurement")
    #    for x in range(0, 60):
    #        self.ui.progressLabel.setText("Time %d" % (x))
    #        time.sleep(1)
        QtGui.qApp.processEvents()

    def LineCleanUp(self):
        self.ui.lblProcess.setText("Clean Up")    
        #End part of sequence
        #Open ion pump (v6)    
        self.v6open()
        for x in range(0, 5):
            self.ui.progressLabel.setText("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        #Open pipettes
        self.ui.lblProcess.setText("Clean Pipettes")       
        self.v2open()
        self.v3open()
        for x in range(0, 5):
            self.ui.progressLabel.setText("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        #close pipettes
        self.v2close()
        self.v3close()
        #wait 5 mins
        self.ui.lblProcess.setText("5 min wait")   
        for x in range(0, 5):
            self.ui.progressLabel.setText("Time %d" % (x))
            time.sleep(1)
            QtGui.qApp.processEvents()
        if self.ui.checkBoxTest.isChecked():
            print "Running In Test Mode - no cleanup on GPIO"
        else:
            pass
            #GPIO.cleanup()
        self.ui.dialGetter.setEnabled(True)
        self.ui.pushButtonAuto.setEnabled(True)
    
        


    def He3Increment(self):
        #Increment the He number by 1
       
        fo = open("Hnum.txt", "r")
        line = fo.readline()
        fo.close()
        HeNum= int(float(line.strip()))
        fo = open("Hnum.txt", "w")
        fo.write(str(HeNum+1))
        fo.close()
        self.UpdateTankNumbers()

    def He4Increment(self):
        #Increment the Q number by 1
       
        fo = open("Qnum.txt", "r")
        line = fo.readline()
        fo.close()
        QNum= int(float(line.strip()))
        fo = open("Qnum.txt", "w")
        fo.write(str(QNum+1))
        fo.close()
        self.UpdateTankNumbers()

 

    def GPIOSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(4,GPIO.OUT)
        GPIO.setup(17,GPIO.OUT)
        GPIO.setup(27,GPIO.OUT)
        GPIO.setup(22,GPIO.OUT)
        GPIO.setup(5,GPIO.OUT)
        GPIO.setup(6,GPIO.OUT)
        GPIO.setup(13,GPIO.OUT)
        GPIO.setup(19,GPIO.OUT)
        GPIO.setup(26,GPIO.OUT)
        GPIO.setup(18,GPIO.OUT)
        GPIO.setup(23,GPIO.OUT)
        GPIO.setup(24,GPIO.OUT)


    def disableButtons(self):
       #Change Buttons to prevent duplication
        self.ui.runAllButton.setEnabled(False)
        self.ui.lbButton.setEnabled(False)
        self.ui.stdButton.setEnabled(False)
        self.ui.sampleButton.setEnabled(False)

    def resetButtons(self):

        self.ui.lblProcess.setText("inactive")               
        self.ui.lbButton.setStyleSheet("background-color: green")
        self.ui.lbButton.setChecked(False)
        self.ui.lbButton.setEnabled(True)
        self.ui.runAllButton.setEnabled(True)
        self.ui.stdButton.setEnabled(True)
        self.ui.sampleButton.setEnabled(True)

    def disableSampleHolder(self):
        self.ui.tableWidgetStandards1.setEnabled(False)
        self.ui.tableWidgetStandards2.setEnabled(False)
        self.ui.tableWidgetSamples.setEnabled(False)
 

        
    def LineBlank(self):
        #show something running
        self.ui.runningButton.setStyleSheet("background-color: orange")
        self.ui.runningButton.setChecked(True)
        #os.system("python /home/pi/PiMS/DisplaySRS/SRSRead.py")

        #Change Button colour
        self.ui.lbButton.setStyleSheet("background-color: orange")
        self.ui.lbButton.setChecked(True)

        self.disableButtons()

        self.ui.lblProcess.setText("Line Blank Started")

        self.RunPrelim()

        self.LoadPipettesSampleBlank()

        self.PreMeasure()
        
        self.QuadMeaure()

        self.LineCleanUp()

        self.resetButtons()


        
        self.ui.runningButton.setStyleSheet("background-color: green")
        self.ui.runningButton.setChecked(False)

    def Extract(self):
        #show something running
        self.ui.runningButton.setStyleSheet("background-color: orange")
        self.ui.runningButton.setChecked(True)


        #Change Button colour
        self.ui.sampleButton.setStyleSheet("background-color: orange")
        self.ui.sampleButton.setChecked(True)

        self.disableButtons()

        self.ui.lblProcess.setText("Extract Started")
        
        self.RunPrelim()

        self.LoadPipettesSampleBlank()

        self.PreMeasure()
        
        self.QuadMeaure()

        self.LineCleanUp()

        #self.resetButtons()

    def ReExtract(self):
        #show something running
        self.ui.runningButton.setStyleSheet("background-color: orange")
        self.ui.runningButton.setChecked(True)


        #Change Button colour
        self.ui.sampleButton.setStyleSheet("background-color: orange")
        self.ui.sampleButton.setChecked(True)

        self.disableButtons()

        self.ui.lblProcess.setText("Re-extract  Started")

        self.RunPrelim()

        self.LoadPipettesSampleBlank()

        self.PreMeasure()
        
        self.QuadMeaure()

        self.LineCleanUp()

        #self.resetButtons()

        
        self.ui.runningButton.setStyleSheet("background-color: green")
        self.ui.runningButton.setChecked(False)        
        
    def RunAllSamples(self):
        print ("Tidy Up Sample Holder")
        self.ui.tableWidgetStandards1.clearSelection()
        self.ui.tableWidgetStandards2.clearSelection()
        self.ui.tableWidgetSamples.clearSelection()
        self.StdTable1()
        self.StdTable2()
        self.SampleTable()
        
        print ("Running All Samples")
        #show something running
        self.ui.runningButton.setStyleSheet("background-color: orange")
        self.ui.runningButton.setChecked(True)
        #os.system("python /home/pi/PiMS/DisplaySRS/SRSRead.py")

        #Change Button colour
        self.ui.runAllButton.setStyleSheet("background-color: yellow")
        self.ui.runAllButton.setChecked(True)


        self.disableButtons()
        self.disableSampleHolder()

        #Initial LB, Q, LB
        self.LineBlank()
        self.QShot()
        self.LineBlank()

        self.disableButtons()
        
        
        #Run First Set of Standards

        for j in range (0,self.ui.tableWidgetStandards1.columnCount()):
            cellText=self.ui.tableWidgetStandards1.item(0,j)
            if cellText is None:
                try:
                    pass
                except:
                    pass
            else:
                if  cellText.text().replace(" ","")=="":
                    self.ui.tableWidgetStandards1.item(0,j).setBackground(QtGui.QColor(255,255,255))
                    self.ui.tableWidgetStandards1.item(0,j).setForeground(QtGui.QColor(0,0,0))
                else:    
                    print(j)
                    SampleHoleNumber=j+10
                    print ("SampleHoleNumber: ", SampleHoleNumber)
                    #Extract
                    self.ui.tableWidgetStandards1.item(0,j).setBackground(QtGui.QColor(255,215,0))
                    self.ui.tableWidgetStandards1.item(0,j).setForeground(QtGui.QColor(0,0,0))
                    #Move to new sample location before continuing
                    QtGui.qApp.processEvents()
                    self.SampleMove(SampleHoleNumber)                   
                    self.Extract()
                    #Re-extract
                    self.ui.tableWidgetStandards1.item(0,j).setBackground(QtGui.QColor(255,165,0))
                    self.ui.tableWidgetStandards1.item(0,j).setForeground(QtGui.QColor(0,0,0))    

                    self.ReExtract()
                        
                    #Finished cell - change to red            
                    self.ui.tableWidgetStandards1.item(0,j).setBackground(QtGui.QColor(255,0,0))
                    self.ui.tableWidgetStandards1.item(0,j).setForeground(QtGui.QColor(255,255,255))    

        #Run Samples
        SampleNumber=0



        for i in range (0,self.ui.tableWidgetSamples.rowCount()):
            for j in range (0,self.ui.tableWidgetSamples.columnCount()):
                cellText=self.ui.tableWidgetSamples.item(i,j)
                if cellText is None:
                    try:
                        pass
                    except:
                        pass
                else:
                    self.ui.tableWidgetSamples.item(i,j).setBackground(QtGui.QColor(0,255,255))
                    self.ui.tableWidgetSamples.item(i,j).setForeground(QtGui.QColor(255,255,255))

                    #EXTRACT
                    SampleHoleNumber=(1+i)*(13+j)
                    print ("SampleHoleNumber: ", SampleHoleNumber)
                            
                    #Extract
                    self.ui.tableWidgetSamples.item(0,j).setBackground(QtGui.QColor(255,215,0))
                    self.ui.tableWidgetSamples.item(0,j).setForeground(QtGui.QColor(0,0,0))
                    #Move to new sample location before continuing
                    QtGui.qApp.processEvents()
                    self.SampleMove(SampleHoleNumber)                   
                    self.Extract()
                    #Re-extract
                    self.ui.tableWidgetSamples.item(0,j).setBackground(QtGui.QColor(255,165,0))
                    self.ui.tableWidgetSamples.item(0,j).setForeground(QtGui.QColor(0,0,0))    

                    self.ReExtract()
                        
                    #Finished cell - change to red            
                    self.ui.tableWidgetSamples.item(0,j).setBackground(QtGui.QColor(255,0,0))
                    self.ui.tableWidgetSamples.item(0,j).setForeground(QtGui.QColor(255,255,255))    

                    SampleNumber=SampleNumber+1

                    if SampleNumber==4:
                        self.LineBlank()
                        SampleNumber=0
                        

                

        #Final LB, Q, LB
        self.LineBlank()
        self.QShot()
        self.LineBlank()


        #Run Second Set of Standards
        for j in range (0,self.ui.tableWidgetStandards2.columnCount()):
            cellText=self.ui.tableWidgetStandards2.item(0,j)
            if cellText is None:
                try:
                    pass
                except:
                    pass
            else:
                if  cellText.text().replace(" ","")=="":
                    self.ui.tableWidgetStandards2.item(0,j).setBackground(QtGui.QColor(255,255,255))
                    self.ui.tableWidgetStandards2.item(0,j).setForeground(QtGui.QColor(0,0,0))
                else:    
                    print(j)
                    SampleHoleNumber=j+62
                    print ("SampleHoleNumber: ", SampleHoleNumber)
                    #Extract
                    self.ui.tableWidgetStandards2.item(0,j).setBackground(QtGui.QColor(255,215,0))
                    self.ui.tableWidgetStandards2.item(0,j).setForeground(QtGui.QColor(0,0,0))
                    #Move to new sample location before continuing
                    QtGui.qApp.processEvents()
                    self.SampleMove(SampleHoleNumber)                   
                    self.Extract()
                    #Re-extract
                    self.ui.tableWidgetStandards2.item(0,j).setBackground(QtGui.QColor(255,165,0))
                    self.ui.tableWidgetStandards2.item(0,j).setForeground(QtGui.QColor(0,0,0))    

                    self.ReExtract()
                        
                    #Finished cell - change to red            
                    self.ui.tableWidgetStandards2.item(0,j).setBackground(QtGui.QColor(255,0,0))
                    self.ui.tableWidgetStandards2.item(0,j).setForeground(QtGui.QColor(255,255,255))    

        
        self.resetButtons()
        
        self.ui.runAllButton.setStyleSheet("background-color: green")
        self.ui.runAllButton.setChecked(True)
        self.ui.runningButton.setStyleSheet("background-color: green")
        self.ui.runningButton.setChecked(False)        

    def QShot(self):
        self.ui.runningButton.setStyleSheet("background-color: orange")
        self.ui.runningButton.setChecked(True)

        #Change Button colour
        self.ui.stdButton.setStyleSheet("background-color: orange")
        self.ui.stdButton.setChecked(True)        

        #Change Buttons to prevent duplication
        self.disableButtons()
        self.ui.lblProcess.setText("Standard Started")
        
        self.RunPrelim()
        
        self.LoadPipettesStandard()


        self.PreMeasure()

        self.QuadMeaure()

        self.LineCleanUp()

        #Reset Buttons
        self.resetButtons()
        self.ui.stdButton.setStyleSheet("background-color: green")
        self.ui.stdButton.setChecked(True)        

    def SampleMove(self, holeNumber):
        print ("Communicate with Arduino to move to hole number ", holeNumber)
        try:
            
            ser = serial.Serial('/dev/ttyACM0', 9600)
            ser.write('\r')
            time.sleep(1)
            ser.write('\r')
            time.sleep(1)

            ser.write(str(holeNumber).encode('utf-8')+'\n')

            s = [0]
            while True:
                read_serial=ser.readline()
                print read_serial

                S = str(read_serial)

                print ("S ",S)
                line = S.split("\\")
                line_int = int(line[0])

                if line_int==1:
                    break

            print "Sample Moved"
        except serial.SerialException, exc:
            print "Arduino error : %s" % exc


if __name__ == "__main__":
  app  = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  app.setStyle('cleanlooks')
  myapp.show()
  sys.exit(app.exec_())
