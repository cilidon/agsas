import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5 import QtGui
from PyQt5.QtPrintSupport import QPrinter
from PyQt5 import QtCore
from PyQt5.QtWidgets import * 
import sys, time
import intuitive as inn
import pandas as pd
import eblue_main as bleu
import train as trainer
a = None
set_f= None
listf=[]
class MainWindow(QDialog):
    

    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui=loadUi("tabletutorial2.ui",self)
        
        self.tableWidget.setAlternatingRowColors(True);
        self.stackedWidget.setCurrentIndex(2)
        self.pushButton.clicked.connect(self.showTable) 
        self.pushButton_2.clicked.connect(self.showText) 
        self.upload.clicked.connect(self.openFileNameDialog) 
        self.cal.clicked.connect(self.start_worker_1)
        self.pushButton_3.clicked.connect(self.saveFileDialog) 
        shadow = QGraphicsDropShadowEffect()
        shadow2 = QGraphicsDropShadowEffect()
  
        # setting blur radius
        shadow2.setBlurRadius(25)
        shadow2.setYOffset(0)
        shadow3 = QGraphicsDropShadowEffect()
  
        # setting blur radius
        shadow3.setBlurRadius(100)
        shadow.setYOffset(0)
        shadow.setXOffset(0)
  
        # setting blur radius
        shadow.setBlurRadius(15)
        shadow.setYOffset(0)
        self.label_4.setFrameStyle(QFrame.Panel | QFrame.Raised)
  
        # adding shadow to the label
       # self.frame_2.setGraphicsEffect(shadow)
       # self.textBrowser.setGraphicsEffect(shadow3)
       
      #  self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)

        self.frame.setGraphicsEffect(shadow2)
        self.home.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2)) 
        self.label_4.setStyleSheet("QLabel{ image: url(resources/no_File.png); background:none;}")
        self.home.setStyleSheet('''QPushButton{  
width: 30%;
 color: #fff;
 image: url(resources/home.png);
  padding: 5px;
  font-size: 18px;
  text-transform: uppercase;
  border-radius: 10px;
border:none;
background: none;
image-position:center;
}
QPushButton:hover{
	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(40, 0, 114, 255), stop:1 rgba(46, 191, 145, 255));
}''')
        self.pushButton_3.setStyleSheet("QPushButton{ image: url(resources/download.png); background:none;} QPushButton:hover{	background-color: rgb(58, 97, 134)}")
        
        #progress_update = QtCore. pyqtSignal(int) 

    def showTable(self): 
     if a:
      if set_f:
       self.loaddata()
       self.stackedWidget.setCurrentIndex(0)
      else:
       self.stackedWidget.setCurrentIndex(4)
       self.label_4.setStyleSheet("QLabel{ image: url(resources/error.png); background:none;}")
       self.label_5.setText("<center>PLEASE CALCULATE FIRST</center>")
     else:
      self.stackedWidget.setCurrentIndex(4)
      
    def openFileNameDialog(self, event):
        global a
        global listf
        global set_f
        set_f= None
        self.cal.setEnabled(True)
        bleu.dfer.qnas.clear()
        self.tableWidget.setSortingEnabled(False)
        if a:
         print(a)
         self.progress_thread.terminate()
         self.progress_thread2.terminate()
        self.label_2.setText("<center>LOADING..........</center>")
        self.progressBar.setValue(0)
        options = QFileDialog.Options()
        #options |= QFileDialog.UseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.txt)", options=options)
        if fileName:
             a = fileName
             listf.clear()
        
        if a:
         self.stackedWidget.setCurrentIndex(1)
         f = open(a,'r',errors="ignore")

         with f:
            data = f.read()
            self.textBrowser.setText(data)
            
        else:
         self.stackedWidget.setCurrentIndex(4)
    def showText(self):
     self.stackedWidget.setCurrentIndex(1)
     if a:
        f = open(a,'r',errors="ignore")

        with f:
            data = f.read()
            self.textBrowser.setText(data)
     else:
      self.stackedWidget.setCurrentIndex(4)
    
    def calculate(self):
      global listf
      global set_f
      
      set_f="hehe"
      intuis = inn.intuitive(a)
      marks=[]
      for i in range(len(inn.df)-1):
       mm=[]
       for j in range(len(inn.df[i])):
        mm.append(inn.df[i].at[j,'marks'] )
       marks.append(mm)
      #marks=[(inn.df[i].at[j,'marks'] for j in range(len(inn.df[i]))) for i in range(len(inn.df))]
      print(marks)
      print(len(intuis))
      bleus=bleu.eblue_init(a)
      print(len(bleus))
      alpha=trainer.train("data/old.txt.txt",a)
      print(alpha)
      var=0
      for i,jj in zip(intuis, bleus) :
       print(len(i))
       print(len(jj))
       print(alpha[var])
       
       fscore=[i[x]*alpha[var] + jj[x]*(1-alpha[var]) for x in range (len (i))]
       var = var+1
       ss=[]
       for j in fscore:
        if j>=4.6:
         ss.append(5)
        elif j>4.2:
         ss.append(4.5)
        elif j>=3.6:
         ss.append(4.0)
        elif j>3.2:
         ss.append(3.5)
        elif j>=2.6:
         ss.append(3.0)
        elif j>2.2:
         ss.append(2.5)
        elif j>=1.6:
         ss.append(2)
        elif j>1.2:
         ss.append(1.5)
        elif j>=0.6:
         ss.append(1)
        else:
         ss.append(0)
       listf.append(ss)
      print(listf)
     
    def start_worker_1(self):
     if a:
      
      self.cal.setEnabled(False)
      
      self.stackedWidget.setCurrentIndex(3)
      self.progress_thread = progressThread()
      self.progress_thread.start()
      self.progress_thread2 = progressThread(value=2)
      self.progress_thread2.start()
      
      self.progress_thread2.progress_update2.connect( self.updateProgressBar)
      self.progress_thread.progress_update.connect( self.updateLabel)
      
     else:
      self.stackedWidget.setCurrentIndex(4)
      
    def updateProgressBar(self, i):
     #self.progressBar.setValue(self.progressBar.value() + maxVal)
     
     if i <=99 and self.progressBar.value  !=100:
      self.progressBar.setValue(i)
     if(i%3==0):
      self.label_2.setText("<center>LOADING&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</center>")
     if(i%3==1):
      self.label_2.setText("<center>LOADING...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</center>")
     elif (i%3==2):
      self.label_2.setText("<center>LOADING......&nbsp;&nbsp;&nbsp;</center>")
     else:
      self.label_2.setText("<center>LOADING.........</center>")
    def updateLabel(self, maxVal):
     if maxVal==1:
      self.label_2.setText("<center>COMPLETED</center>")
      self.progressBar.setValue(100)

    
    def saveFileDialog(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Sheets (*.xlsx)", options=options)
        if fileName:
            self.df=self.df.sort_values('sid')
            self.df.to_excel(fileName,index=False)
    def loaddata(self):
        ll=["Sid"]
        self.tableWidget.setSortingEnabled(False)
        ssid=[]
        dictt={}
        self.l = len(listf)
        col=1
        self.tableWidget.setColumnCount(self.l+1);
        self.stackedWidget.setCurrentIndex(2)

        
        for i in range(self.l+1):
         self.tableWidget.setColumnWidth(i,10)
        
        for i in range(self.l):
         ll.append("Question "+str(i+1))
         
         
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setRowCount(len(listf[0]))
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setHorizontalHeaderLabels(ll)
        for j in range(len(inn.df[0].index)):
          self.tableWidget.setItem(j,0 , QtWidgets.QTableWidgetItem(inn.df[0].at[j,'sid'] ))
          ssid.append(inn.df[0].at[j,'sid'] )
          self.tableWidget.item(j, 0).setBackground(QtGui.QColor(96, 102, 155))
          self.tableWidget.item(j, 0).setForeground(QtGui.QColor(255, 255, 255))
          self.tableWidget.item(j, 0).setTextAlignment(QtCore.Qt.AlignCenter)
          self.tableWidget.item(j, 0).setFont(QtGui.QFont('Microsoft YaHei', 10))
          
        dictt['sid']=ssid
        for i in range(len(listf)):
         dictt[ll[i+1]]=listf[i]
        self.df = pd.DataFrame(dictt)
        for i in listf:
         row=0
         for j in i:
          #j=
          self.tableWidget.setItem(row,col , QtWidgets.QTableWidgetItem(str(j)))
          self.tableWidget.item(row, col).setTextAlignment(QtCore.Qt.AlignCenter)
          self.tableWidget.item(row, col).setFont(QtGui.QFont('Microsoft YaHei', 8))
          
          row = row+1
         col=col+1
        
        
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

        print(self.df)
class progressThread(QtCore.QThread):

    progress_update = QtCore. pyqtSignal(int)
    progress_update2 = QtCore.pyqtSignal(int)
    

    def __init__(self, value = 1):
        QtCore.QThread.__init__(self)
        self.value = value

    def __del__(self):
        self.wait()


    def run(self):
        if self.value==1:
         MainWindow.calculate(self)
        
        # your logic here
        i=0
        while 1:      
            i=i+1
            maxVal = 1 # NOTE THIS CHANGED to 1 since updateProgressBar was updating the value by 1 every time
            self.progress_update.emit(maxVal)
            if self.value==2:
             time.sleep(0.4)
            # Tell the thread to sleep for 1 second and let other things run
            self.progress_update2.emit(i)
            time.sleep(0.002)

# main
app = QApplication(sys.argv)
mainwindow = MainWindow()
 
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setMinimumHeight(750)
widget.setMinimumWidth(1120)
widget.setWindowTitle("Automatic Grader")
widget.setWindowIcon(QIcon("resources/icon.png"))
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")
