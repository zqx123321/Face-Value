# -*- coding: utf-8 -*-
import urllib  
import urllib2  
import cookielib  
import re
import base64
import json
import time


#很重要！！！！！！！！！！！！！！！！
######################################################################
cookie_support= urllib2.HTTPCookieProcessor(cookielib.CookieJar())
opener = urllib2.build_opener(cookie_support)
urllib2.install_opener(opener)

#访问首页，获取cookie
firstURL = 'http://kan.msxiaobing.com/V3/Portal?task=yanzhi&ftid='
request = urllib2.Request(firstURL)  
response = urllib2.urlopen(request)  
content = response.read()
######################################################################

def UploadBase64(usercode): 

	#从我们学校查宿舍网站获取照片，把这段代码换成读本地照片也可以
	################################################################################
	url='http://hqxsgy.ouc.edu.cn/uploadfile/image/photos/20161026/'+usercode+'.jpg'
	request = urllib2.Request(url)  
	response = urllib2.urlopen(request)  
	content = response.read()
	################################################################################

	b64=base64.b64encode(content) #读取文件内容，转换为base64编码
	#print b64

	headerdic={  
	     'User-Agent':
	        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	}  
	


	LoginUrl='https://kan.msxiaobing.com/Api/Image/UploadBase64'
	request = urllib2.Request(LoginUrl,b64, headerdic)  
	response = urllib2.urlopen(request)  
	res=json.loads( response.read())

	return res["Host"]+res["Url"]


def getScore(usercode):

	headerdic={  
	     'User-Agent':
	        'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
		 'Referer':'http://kan.msxiaobing.com/V3/Portal?task=yanzhi&ftid=',
		 'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',

	}  

	res=UploadBase64(usercode)

	t=time.time()
	postdic={
	'MsgId':str(int(t*1000)),
	'CreateTime':str(int(t)),
	'Content[imageUrl]':res,
	}

	
	  

	postData=urllib.urlencode(postdic)

	LoginUrl='http://kan.msxiaobing.com/Api/ImageAnalyze/Process?service=yanzhi&tid='
	request = urllib2.Request(LoginUrl,postData, headerdic)  
	response = urllib2.urlopen(request)  
	result=json.loads(response.read())
	content=result["content"]
	text= content["text"]
	score= filter(str.isdigit, str(text))
	print usercode,score[0]+"."+score[1]

			

if __name__ == "__main__":
	for i in range(15020031001,15020031123):
		#try:
		getScore(str(i))
		# except:
		# 	print "Error"+str(i)
              

