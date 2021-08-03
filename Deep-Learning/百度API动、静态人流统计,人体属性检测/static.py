# encoding:utf-8

#import requests
import base64
import json
import urllib.request
'''
人流量统计
'''

request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_num"
# 二进制方式打开图片文件
f = open('E:\pedestrian_volume/wuxing4-out.jpg','rb')
img = base64.b64encode(f.read())


def save_base_image(img_str, filename):
  img_data = base64.b64decode(img_str)
  with open(filename, 'wb') as f:
    f.write(img_data)

params = dict()
params['image'] = img
params['show'] = 'true'
params = urllib.parse.urlencode(params).encode("utf-8")


access_token = '24.5780bbb88a1048cf987c61e304f9da91.2592000.1622033457.282335-24071671'#替换成你的token
request_url = request_url + "?access_token=" + access_token
#response = requests.post(request_url, data=params, headers=headers)
requests = urllib.request.Request(url=request_url, data=params)
requests.add_header('Content-Type', 'application/x-www-form-urlencoded')
response = urllib.request.urlopen(requests)
content = response.read()
if content:
    # print(content)
    content = content.decode('utf-8')
    # print(content)
    data = json.loads(content)
    # print(data)
    person_num = data['person_num']
    print('person_num', person_num)
    img_str = data['image']
    save_base_image(img_str, 'E:\pedestrian_volume/wuxing4-out-1.jpg')