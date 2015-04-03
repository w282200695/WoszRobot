#Get global bing's background
#developer : wosz
#Time 2015/4/3 22:43

import re
import urllib

def gethtml(url):
     html = urllib.urlopen(url).read()
     return html

def getimage(html):
     address_re  = r'url\":\"(.*)\",\"urlbase'
     filename_re = r'rb/(.*)_EN'
     address_r   = re.compile(address_re)
     filename_r  = re.compile(filename_re)
     address_l   = re.findall(address_r,html)
     filename_l  = re.findall(filename_r,address_l[0])
     address     = "http://global.bing.com"+address_l[0]
     filename    = filename_l[0]+".jpg"
     print filename + " Downing."
     urllib.urlretrieve(address,filename)
     print filename + " Finished."

#--------------------------------main-----------------------------------

number = input("please input a number : ")
for num in range(number):
     url = "http://global.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=1\
     &pid=hp&setmkt=en-us" %num
     getimage(gethtml(url))
print "All Done."
