# encoding:utf-8
import cv2
import requests
import base64
import  pandas as pd
'''
人体检测和属性识别
'''
#API路由
request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_attr"
# 二进制方式打开图片文件
f = open('E:\pedestrian_volume/body/wuxing0-out.jpg', 'rb')
img1 = cv2.imread('E:\pedestrian_volume/body/wuxing0-out.jpg')
img = base64.b64encode(f.read())
#请求参数
params = {"image":img}
#发送请求
access_token = '*************************************************'#替换成你的token
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
#打印返回结果
if response:
    print (response.json())
content = response.json()
#保存数据
df = pd.DataFrame.from_dict(data=content['person_info'], orient='columns')
df.to_csv('test.csv')
df.head()
#绘制检测框
for i in range(0,12):
    left_top = (int(content['person_info'][i]['location']['left']), int(content['person_info'][i]['location']['top']))
    right_bottom = (int(left_top[0] + content['person_info'][i]['location']['width']),int(left_top[1] + content['person_info'][i]['location']['height']))
    cv2.rectangle(img1, left_top, right_bottom, (0, 0, 255), 2)
cv2.namedWindow('img1', cv2.WINDOW_NORMAL) #定义窗口
cv2.imshow('img1', img1) #查看返回带检测框图片
cv2.imwrite('body.png',img1)  # 写入图片
cv2.waitKey(0)