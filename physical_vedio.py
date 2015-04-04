#A Robot That Can Download GDUT Physical Experiment Vedio
#Developer: Wosz
#Time: 2015/4/4 10:31
# -*- coding: UTF-8 -*-
import re
import urllib
import sys

global a
def gethtml(url):               #读取网页
	html = urllib.urlopen(url).read()
	return html

def diff(son_address):          #文件名去重
        new_son_address = []
        for son in son_address:
             if son not in new_son_address:
                  new_son_address.append(son)
        return new_son_address

def report(count, blockSize, totalSize): #下载进度的回调函数
    global a
    percent = int(count*blockSize*100/totalSize)
    if(percent!= a):
            sys.stdout.write("\r%d%% " % percent)
            sys.stdout.flush()
            a = percent
            if(percent%10 == 0): print
    
def downloadvedio(filename,url):#下载视频
	address = url+"images/"+filename
	print filename + " Downloading."
	global a
	a = 0
	urllib.urlretrieve(address,filename, reporthook=report)
	print filename + " Finish."
	
def get_son_address(html):      #获取子网页地址
	htm_re = r'a href=\"(.*)\" target'
	htm_r  = re.compile(htm_re)
	htm_l  = re.findall(htm_r,html)
	htm_ld = diff(htm_l)
	return htm_ld
	
def get_file_name(son_html):    #获取视频文件名
	filename_re = r'vcastr_file\=(.*)\">'
	filename_r  = re.compile(filename_re)
	filename_l  = re.findall(filename_r,son_html)
	filename    = filename_l[0]
	return filename

def get_father_address(url):    #获取url的路径
	father_re = r'(.*/)'
	father_r  = re.compile(father_re)
	father_l  = re.findall(father_r,url)
	father_address = father_l[0]
	return father_address
	
#--------------------------------------main-----------------------------------------------

url = raw_input("Input The URL :\n")
#url = "http://222.200.98.186:8088/FileUpload/demo/静电场模拟描迹/实验演示.htm"
head = get_father_address(url)
son_list = get_son_address(gethtml(url))
for son in son_list:
     son_address = head + son
     downloadvedio(get_file_name(gethtml(son_address)),head)
print "All Done. Bye,Bye"
