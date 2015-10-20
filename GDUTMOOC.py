from PyQt4 import QtCore, QtGui
import sys
import webbrowser
import os
import re
import urllib
import urllib2

class UI(QtGui.QWidget):
    htmlLabel = ''
    htmlLine = ''
    htmlBtn = ''
    htmlPath = ''
    analysisBth = ''
    indexBtn = ''
    closeBtn = ''
    numberLabel = ''
    numberLine = ''
    number = 0
    startBtn = ''
    mainLayout = ''

    Chapter = []
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.init()
        self.initConnection()
        self.setLayout(self.mainLayout)


    def init(self):
        self.htmlLabel = QtGui.QLabel()
        self.htmlLabel.setText("HTML PATH ")
        self.htmlLine = QtGui.QLineEdit()
        self.htmlLine.setDisabled(True)
        self.htmlBtn = QtGui.QPushButton()
        self.htmlBtn.setText("...")
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.htmlLabel)
        topLayout.addWidget(self.htmlLine)
        topLayout.addWidget(self.htmlBtn)
        self.analysisBth = QtGui.QPushButton()
        self.analysisBth.setText("Analysis")
        self.indexBtn = QtGui.QPushButton()
        self.indexBtn.setText("MOOC")
        self.closeBtn = QtGui.QPushButton()
        self.closeBtn.setText("Close")
        midLayout = QtGui.QHBoxLayout()
        midLayout.addWidget(self.analysisBth)
        midLayout.addWidget(self.indexBtn)
        midLayout.addWidget(self.closeBtn)
        self.numberLabel = QtGui.QLabel()
        self.numberLabel.setText("Browser N:")
        self.numberLine = QtGui.QLineEdit()
        self.numberLine.setText("1")
        self.startBtn = QtGui.QPushButton()
        self.startBtn.setText("Start")
        bottomLayout = QtGui.QHBoxLayout()
        bottomLayout.addWidget(self.numberLabel)
        bottomLayout.addWidget(self.numberLine)
        bottomLayout.addWidget(self.startBtn)
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addItem(topLayout)
        self.mainLayout.addItem(midLayout)
        self.mainLayout.addItem(bottomLayout)
        self.setFixedWidth(550)
        self.setWindowTitle("GDUT MOOC")

    def initConnection(self):
        QtCore.QObject.connect(self.htmlBtn,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("pathDialog()"))
        QtCore.QObject.connect(self.closeBtn,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("close()"))
        QtCore.QObject.connect(self.analysisBth,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("analisisEvent()"))
        QtCore.QObject.connect(self.indexBtn,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("indexEvent()"))
        QtCore.QObject.connect(self.startBtn,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("startEvent()"))

    @QtCore.pyqtSlot()
    def pathDialog(self):
        self.htmlPath = QtGui.QFileDialog.getOpenFileName(self,"HTML FILE",".","HTML Files(*.html *.htm)")   #保存地址选择
        self.htmlLine.setText(self.htmlPath)

    @QtCore.pyqtSlot()
    def analisisEvent(self):
        if len(self.htmlPath) == 0:
            self.htmlLine.setText("PATH IS EMPTY !!!")
        else:
            tool = analysisTool(self.htmlPath)
            tool.read()
            tool.search()
            tool.output()
            self.Chapter = tool.chapterlist
            self.htmlLine.setText("Analysis Finished.")

    @QtCore.pyqtSlot()
    def startEvent(self):
        self.number = int(self.numberLine.text())
        if os.path.isfile("data.txt") == False:
            self.htmlLine.setText("data.txt is not exists, Analysis First.")
        else:
            if len(self.Chapter) == 0:
                f = open('data.txt','r')
                k = f.read()
                f.close()
                k = k.split('\n')
                for g in range(0,len(k)-1,3):
                    self.Chapter.append((k[g],k[g+1],k[g+2]))
            temp = self.Chapter
            while len(self.Chapter) >0:    
                if self.number == 0:
                    break
                i = self.Chapter.pop(0)
                url = 'http://mooc1-1.chaoxing.com/mycourse/studentstudy?courseId=%s&clazzid=%s&chapterId=%s' % (i[0],i[1],i[2])
                webbrowser.open(url,0)
                self.number = self.number - 1
            f = open('data.txt','w+')
            for i in self.Chapter:
                for j in i:
                    f.write(j)
                    f.write("\n")
            f.close()

    @QtCore.pyqtSlot()
    def indexEvent(self):
        url = "http://gdut.benke.chaoxing.com/portal"
        webbrowser.open_new(url)

class analysisTool:
    path = ''
    htmlData = ''
    chapterlist = []
    def __init__(self):
        self.path = ''

    def __init__(self,path):
        self.path = path
    
    def analysis(self):
        self.read()
        self.search()
        self.output()

    def read(self):
        f = open(self.path,'r')
        self.htmlData = f.read();
        f.close()

    def search(self):
        #rc = re.compile(r'courseId=(.*)&classId=(.*)&chapterId=(.+?)&[\s\S]+?<a.+?title="(.*)"')
        self.chapterlist = []
        rc1 = re.compile(r'target="_blank" href="(.*)">[\s]+?<span class="zadd_s_notComplete"')
        tmp = re.findall(rc1,self.htmlData)
        rc = re.compile(r'courseId=(.*)&classId=(.*)&chapterId=(.+?)&')
        for i in tmp:
            k = re.findall(rc,i)
            self.chapterlist.append(k[0])

    def output(self):
        f = open('data.txt','w+')
        for i in self.chapterlist:
            for j in i:
                f.write(j)
                f.write("\n")
        f.close()

#--------------------MAIN-------------------

sys.path.append("libs")
app = QtGui.QApplication(sys.argv)
os.system("mode con cols=20 lines=1 ")
window = UI()
window.show()
sys.exit(app.exec_())
