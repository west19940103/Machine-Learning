import cv2
import base64
from PIL import Image
from io import BytesIO
import requests
import json
import numpy as np
import threading
import time
import subprocess as sp

shared_image = (np.ones((540, 960, 3), dtype=np.uint8) * 255).astype(np.uint8)
process_image = (np.ones((540, 960, 3), dtype=np.uint8) * 255).astype(np.uint8)

# 左上角
# 右上角
# 左下角
# 右下角
# area 代表的是要检测的区域范围
def getResult(img):
    params = {
        "area": "1,1,     590,1,    590,190,     1,190",
        "case_id": 1,
        "case_init": "false",
        "dynamic": "true",
        "image": img,
        "show": "true", }
    # 请求参数
    request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_tracking"
    access_token = '24.5780bbb88a1048cf987c61e304f9da91.2592000.1622033457.282335-24071671'
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.post(request_url, data=params, headers=headers)

    if response:
        # 将 Python 字典类型转换为 JSON 对象
        # print(response.json())
        json_str = json.dumps(response.json())
        # 转化为 json字符串
        d = json.loads(json_str)

        # print(d['image'])
        # print(d['person_count'])
        person_count = d['person_count']
        in_num = person_count['in']
        out_num = person_count['out']
        print("in: ", in_num)
        print("out: ", out_num)
        # 再把加密后的结果解码， 结果为二进制数据
        temp = base64.b64decode(d['image'])
        # print(temp)
        # 二进制数据流转np.ndarray [np.uint8: 8位像素]
        img = cv2.imdecode(np.frombuffer(temp, np.uint8), cv2.IMREAD_COLOR)
        #   将bgr转为rbg
        rgb_img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # print(rgb_img)
        # cv2.imshow("res", rgb_img)
        # cv2.waitKey()
        return rgb_img

def frame2base64(frame):
    img = Image.fromarray(frame)  # 将每一帧转为Image
    output_buffer = BytesIO()  # 创建一个BytesIO
    img.save(output_buffer, format='JPEG')  # 写入output_buffer
    byte_data = output_buffer.getvalue()  # 在内存中读取
    base64_data = base64.b64encode(byte_data)  # 转为BASE64
    return base64_data  # 转码成功 返回base64编码

def generate():
    camera = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = camera.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("camera", frame)
            base64_data = frame2base64(frame)

            getResult(base64_data)

            # print(base64_data)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except Exception as e:
        print(e)
    finally:
        # 释放资源
        camera.release()
        cv2.destroyAllWindows()
    return  base64_data

# 定义CV线程， 提取视频流 抽帧
class CvThread(threading.Thread):
    def __init__(self):
        super(CvThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        # self.arg=arg
    def run(self):  # 定义每个线程要运行的函数
        print('CvThread thread is run!')
        global shared_image
        camera = cv2.VideoCapture(0)
        if (camera.isOpened()):
            print('Open camera 1')
        else:
            print('Fail to open camera 1!')
            time.sleep(0.05)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 864)  # 2560x1920 2217x2217 2952×1944 1920x1080
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera.set(cv2.CAP_PROP_FPS, 5) # 抽帧参数
        size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)), int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        sizeStr = str(960) + 'x' + str(540)
        fps = camera.get(cv2.CAP_PROP_FPS)  # 30p/self
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('res_mv.avi', fourcc, fps, size)
        while True:
            ret, frame = camera.read()  # 逐帧采集视频流
            if frame is not None:
                image = Image.fromarray(frame)
                image = image.resize((960, 540))
                frame = np.array(image)
                # cv2.imwrite('F:/renliu/chouzhen/'+ str(i) +'.jpg',frame)
                # print(frame)
                shared_image = frame

# 定义检测线程， 检测视频
class BaiDuThread(threading.Thread):
    def __init__(self):
        super(BaiDuThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。

    def run(self):  # 定义每个线程要运行的函数
        print('BaiDuThread thread is run!')
        global shared_image
        global process_image
        while True:
            # 把图片编码
            img = Image.fromarray(shared_image)  # 将每一帧转为Image
            output_buffer = BytesIO()  # 创建一个BytesIO
            img.save(output_buffer, format='JPEG')  # 写入output_buffer
            byte_data = output_buffer.getvalue()  # 在内存中读取
            base64_data = base64.b64encode(byte_data)  # 转为BASE64
            res = getResult(base64_data)
            process_image = res
            time.sleep(0.05)

RTMP_HOST = '192.168.0.208'
rtmpUrl = 'rtmp://' + RTMP_HOST + ':1935/live/test3'
#rtp = 'rtp://@:1234'
command = ['ffmpeg',
    '-y',
    '-f', 'rawvideo',
    '-vcodec','rawvideo',
    '-pix_fmt', 'bgr24',
    '-s', '960x540',
    '-r', str(5),
    '-i', '-',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'ultrafast',
    '-f', 'flv',
    rtmpUrl]

global pipe
pipe = sp.Popen(command, stdin=sp.PIPE)

class PushThread(threading.Thread):
    def __init__(self):
        super(PushThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        # self.arg=arg
    def run(self):  # 定义每个线程要运行的函数
        print('PushThread thread is run!')
        global process_image
        while True:
            pipe.stdin.write(process_image.tostring())  # 存入管道
            cv2.imwrite('1.jpg',process_image)
            time.sleep(0.198)

CvThread = CvThread()
CvThread.start()

BaiDuThread = BaiDuThread()
BaiDuThread.start()

PushThread = PushThread()
PushThread.start()