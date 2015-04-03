#一个爬bing壁纸的爬虫。
#developer：Wosz
#第一次玩PY，代码风格很乱，很容易逼死强迫症

#code = utf-8
import re
import urllib

def gethtml(url):
	page = urllib.urlopen(url)
	html = page.read()
	return html

#以下是显示下载进度的函数，由于丑了一逼，我就把它注释掉了
#def report_hook(count, block_size, total_size):
#        print '%02d%%'%(100.0 * count * block_size/ total_size)

def getimage(html):
	reg = r'url\"\:\"(.+?)\",\"urlbase'
	image = re.compile(reg)
	imglist = re.findall(image,html)
	file_name = re.compile(r'rb/(.*)_Z')
	file_name_list = re.findall(file_name,imglist[0])
	filename = file_name_list[0]+".jpg"
	#print file_name_list     我调试的时候用的。
	#print html
	print filename+" downloading.."
	urllib.urlretrieve(imglist[0],filename)
	print filename+" finish downloading."

#------------------------------main--------------------------------------
max1 = input("please input a number which < 16: ")
for a in range(max1):
        url = "http://cn.bing.com/HPImageArchive.aspx?format=js&idx=%d&n=1" %a
        html = gethtml(url)
        getimage(html)
print "All Done"
