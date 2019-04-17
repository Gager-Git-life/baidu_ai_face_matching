#coding:utf-8
from collections import OrderedDict
import requests
import os,sys
import json
import base64
import cv2


face_id = ''
request_url = "https://aip.baidubce.com/rest/2.0/face/v3/match"
# client_id 为官网获取的AK， client_secret 为官网获取的SK
get_token_host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=n6ST7v09nrNM4vAFeSzlFR8j&client_secret=RmoX4IvG2mOO3PciCU2t1FMdb2OpGyAA'
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
access_token = ''

def get_token(host):
	global access_token
	response = requests.get(host,headers=header, verify=False)
	if response.status_code != 200:
		print(u'[INFO]>>> 获取token失败')
		sys.exit(0)
	else:
		access_token = json.loads(response.text)['access_token']
		print(u'[INFO]>>> 获取成功:{}'.format(access_token))
		#print(u'[INFO]>>> 证书类型:{}'.format(type(access_token)))
		
get_token(get_token_host)

def face_detection(pic1,pic2):
	global request_url,access_token
	f = open(pic1, 'rb')
	# 参数images：图像base64编码
	img1 = base64.b64encode(f.read())
	# 二进制方式打开图文件
	f = open(pic2, 'rb')
	# 参数images：图像base64编码
	img2 = base64.b64encode(f.read())

	params = json.dumps(
    [{"image": img1, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"},
     {"image": img2, "image_type": "BASE64", "face_type": "LIVE", "quality_control": "LOW"}])
	request_url = request_url + "?access_token=" + access_token
	#print('[INFO]>>> request url:{}'.format(request_url))
	try:
		response = requests.post(url=request_url, data=params, headers=header,verify=False)
		response.raise_for_status()
		content = json.loads(response.text)['result']['score']
		if content:
			print content
			return content
		else:
			return 0
	except Exception as e:
		print(u'[INFO]>>> 出现错误:{}'.format(e))
		return 0
		
#face_detection('test1.jpg','test2.jpg')

def draw_box(pic):
	global face_id
	img = cv2.imread(pic,cv2.IMREAD_COLOR)
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")
	faces = face_cascade.detectMultiScale(gray, 1.3, 5)
	for (x,y,w,h) in faces:
		img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(img, face_id, (x,y-10),font , 0.8 ,(0,0,255),2)
	cv2.namedWindow('result',cv2.WINDOW_AUTOSIZE)
	cv2.imshow('result',img)
	if(cv2.waitKey(0) == ord('q')):
		cv2.destroyAllWindows()
	

#读取本地图片路径
detect_dict = OrderedDict()
test_pic = 'test.jpg'
pic_path = os.getcwd() + '\\' + 'save_pic\\'
for pic in os.listdir(pic_path):
	pic_id = pic.split('.jpg')[0]
	ab_pic_path = pic_path + '\\' + pic
	#print(u"[INFO]>>> 当前测试图片绝对地址:{}".format(ab_pic_path))
	score = face_detection(ab_pic_path,test_pic)
	detect_dict[pic_id] = score
	if(score > 90):
		break
	#print(u'[INFO]>>> 检测结果为:{}'.format(score))

max_score = max(zip(detect_dict.values(), detect_dict.keys()))
min_score = min(zip(detect_dict.values(), detect_dict.keys()))
face_id = max_score[1]
print(u'[INFO]>>> 最有可能是:{}  最不可能是:{}'.format(max_score[1],min_score[1]))
	
#draw_box(pic_path +face_id+ '.jpg')
draw_box('test.jpg')


