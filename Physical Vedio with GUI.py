# 2015-09-13 01:09:14 update
# designer：wosz
# BUG：update UI from another thread (fixed)
# -*- coding: UTF-8 -*-
import sys
import re
import urllib
import sys
import threading
import os
from PyQt4 import QtCore, QtGui

class UI(QtGui.QWidget):
    url_text = 0            #视频地址
    mainLayout = 0          #主窗体UI框架
    missionLayout = 0       #任务UI框架
    startBtn = 0            
    closeBtn = 0
    pathBtn = 0
    path = ''               #保存文件路径
    pathLabel = 0           #显示设定的文件保存路径
    threadArray = []        #线程数组
    progressBarArray = []   #进度条数组

    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.init()                     #界面初始化
        self.bulidConnection()          #信号-槽连接
        self.setLayout(self.mainLayout)
        self.setWindowIcon(QtGui.QIcon(urlTool.cur_file_dir()+"//main.ico"))

    def bulidConnection(self):
        QtCore.QObject.connect(self.closeBtn, QtCore.SIGNAL("clicked()"),self, QtCore.SLOT("CloseEvent()"))
        QtCore.QObject.connect(self.startBtn,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("startSignal()"))
        QtCore.QObject.connect(self.pathBtn,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("pathDialog()"))

    def init(self):         #界面构建
        self.missionLayout = QtGui.QVBoxLayout()    
        self.mainLayout = QtGui.QVBoxLayout()
        self.setWindowTitle("Download Tool")
        self.url_text = QtGui.QLineEdit()
        url_label = QtGui.QLabel("url:")
        url_label.setFixedWidth(25)
        top_Hlayout = QtGui.QHBoxLayout()
        top_Hlayout.addWidget(url_label)
        top_Hlayout.addWidget(self.url_text)
        self.startBtn = QtGui.QPushButton()
        self.startBtn.setText("START")
        self.closeBtn = QtGui.QPushButton()
        self.closeBtn.setText("CLOSE")
        self.pathBtn = QtGui.QPushButton()
        self.pathBtn.setText("PATH")
        secondHlayout = QtGui.QHBoxLayout()
        self.pathLabel = QtGui.QLineEdit()
        self.pathLabel.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.pathLabel.setText("Directory Path")
        self.pathLabel.setDisabled(True)
        #secondHlayout.addSpacerItem(QtGui.QSpacerItem(200,0,QtGui.QSizePolicy.Expanding))
        secondHlayout.addWidget(self.pathLabel)
        secondHlayout.addWidget(self.pathBtn)
        secondHlayout.addWidget(self.startBtn)
        secondHlayout.addWidget(self.closeBtn)
        self.mainLayout.addLayout(top_Hlayout)
        self.mainLayout.addLayout(secondHlayout)
        self.mainLayout.addLayout(self.missionLayout)

        

    def addMission(self,fileName,processBar):   #添加任务
        layout = QtGui.QVBoxLayout()
        nameLabel = QtGui.QLabel(fileName+" Downloading")
        layout.addWidget(nameLabel)
        layout.addWidget(processBar)
        layout.setMargin(0)
        self.missionLayout.addLayout(layout)
    
    @QtCore.pyqtSlot()
    def startSignal(self):  #响应startBtn 启动爬虫
        if(self.url_text.text().isEmpty()):
            QtGui.QMessageBox.information(self,"Warning","url is empty")        #地址为空
        elif(len(self.threadArray) == 0):
            url = str(self.url_text.text().toUtf8())
            head = urlTool.get_father_address(url)
            son_list = urlTool.get_son_address(urlTool.gethtml(url))
            id = 0
            for son in son_list:
                sonAddress = head + son
                son = downloadThread(urlTool.get_file_name(urlTool.gethtml(sonAddress)),head,self.path,id)  #任务类实例化
                self.addMission(son.fileName,son.QprcessBar)
                self.progressBarArray.append(son.QprcessBar)
                th = threading.Thread(target = son.start,args = ())     #为任务创建线程
                th.setDaemon(True)
                QtCore.QObject.connect(son,QtCore.SIGNAL("updateSignal(int,int)"),self,QtCore.SLOT("update(int,int)"))  #连接任务类的信号以进行主线程UI刷新
                self.threadArray.append(th)
                th.start()
                id = id + 1
        else:
            QtGui.QMessageBox.information(self,"Warning","there is something wrong.")

    @QtCore.pyqtSlot()
    def pathDialog(self):
        self.path = QtGui.QFileDialog.getExistingDirectory() + '\\'     #保存地址选择
        self.pathLabel.setText(self.path)

    @QtCore.pyqtSlot()
    def CloseEvent(self):       #关闭程序并询问是否结束正在进行的任务
        done = True
        for thread in self.threadArray:
            if(thread.isAlive()):
                done = False
                break

        if(done == False):
            q = QtGui.QMessageBox.question(self,"Close?","Discard all tasks ?",QtGui.QMessageBox.Ok|QtGui.QMessageBox.No,QtGui.QMessageBox.No)
            if q == QtGui.QMessageBox.Ok:
                self.close()                
        else:
            self.close()


    @QtCore.pyqtSlot(int,int)
    def update(self,id,percent):        #主线程中更新进度条
        self.progressBarArray[id].setValue(percent)




        
class downloadThread(QtCore.QObject):   #任务类
    fileName = ''
    fileAddress = ''
    path = ''
    precent = 0
    QprcessBar = 0
    ID = 0
    updateSignal = 0
    def __init__(self,fileName,addressHead,path,id):
        QtCore.QObject.__init__(self)
        self.fileAddress = addressHead+"images/"+fileName
        self.fileName = fileName
        self.QprcessBar = QtGui.QProgressBar()
        self.QprcessBar.setMaximum = 100
        self.QprcessBar.setMinimum = 0
        self.path = path
        self.ID = id
        self.updateSignal = QtCore.pyqtSignal(int,int)


    def start(self):
        urllib.urlretrieve(self.fileAddress,self.path + self.fileName, reporthook=self.report)      #开始下载

    def report(self,count, blockSize, totalSize): #下载进度的回调函数
        percent = int(count*blockSize*100/totalSize)
        if(percent != self.precent):
            #self.QprcessBar.setValue(percent)
            self.precent = percent
            self.emit(QtCore.SIGNAL('updateSignal(int,int)'),self.ID,percent)   #焕发更新进度条UI信号

class urlTool(object):
    @staticmethod
    def get_father_address(url):    #获取url的路径
        father_re = r'(.*/)'
        father_r  = re.compile(father_re)
        father_l  = re.findall(father_r,url)
        father_address = father_l[0]
        return father_address

    @staticmethod
    def get_file_name(son_html):    #获取视频文件名
        filename_re = r'vcastr_file\=(.*)\">'
        filename_r  = re.compile(filename_re)
        filename_l  = re.findall(filename_r,son_html)
        filename    = filename_l[0]
        return filename

    @staticmethod
    def get_son_address(html):      #获取子网页地址
        htm_re = r'a href=\"(.*)\" target'
        htm_r  = re.compile(htm_re)
        htm_l  = re.findall(htm_r,html)
        htm_ld = urlTool.diff(htm_l)
        return htm_ld

    @staticmethod
    def diff(son_address):          #文件名去重
        new_son_address = []
        for son in son_address:
             if son not in new_son_address:
                  new_son_address.append(son)
        return new_son_address

    @staticmethod
    def gethtml(url):               #读取网页
        html = urllib.urlopen(url).read()
        return html

    @staticmethod
    def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

#---------------------------Main------------------------
app = QtGui.QApplication(sys.argv)
window = UI()
window.show()
sys.exit(app.exec_())
