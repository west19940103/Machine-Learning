import requests
import base64
import os
import cv2
# 视频文件名字
filename = r'E:\pedestrian_volume/xiaochijie.mp4'
# 视频帧率12
fps = 12
# 保存图片的帧率间隔
count = 6
# 开始读视频
videoCapture = cv2.VideoCapture(filename)
i = 0
j = 0
while True:
    success, frame = videoCapture.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("camera", frame)
    i += 1
    if (i % count == 0):
        # 保存图片
        j += 1
        try:
            savedname = filename.split('.')[1] + '_' + str(j) + '.jpg'
            cv2.imwrite("E:\pedestrian_volume\image1/" + savedname, frame)
            print('image of %s is saved' % (savedname))

            request_url = "https://aip.baidubce.com/rest/2.0/image-classify/v1/body_tracking"
            # 二进制方式打开图片文件
            f = open("E:\pedestrian_volume\image1/" + savedname, 'rb')
            img = base64.b64encode(f.read())

            params = {"area": "1,1,   520,1,     520,900,   1438,900,     1438,1438,  1,1438","case_id":3,
                      "case_init": "false", "dynamic": "true", "image": img,"show": "true"}
            access_token = '24.5780bbb88a1048cf987c61e304f9da91.2592000.1622033457.282335-24071671'#替换成你的token
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                with open(f"E:\pedestrian_volume\image1/{savedname}", 'wb') as f:
                    f.write(base64.b64decode(response.json()['image']))
        except:
            continue

    if not success:
        path = 'E:\pedestrian_volume\image1/'
        filelist = os.listdir(path)

        img = cv2.imread(path + filelist[0])
        # 打印图像的分辨率
        print(img.shape)  # (3840, 2160, 3)
        fps = 5  # 视频每秒24帧
        size = (img.shape[1], img.shape[0])  # 需要转为视频的图片的尺寸
        # 可以使用cv2.resize()进行修改

        video = cv2.VideoWriter(filename.split(".")[1]+"_return1.avi", cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps, size)
        # 视频保存在当前目录下

        for item in filelist:
            if item.endswith('.jpg'):
                # 找到路径中所有后缀名为.png的文件，可以更换为.jpg或其它
                item = path + item
                img = cv2.imread(item)
                video.write(img)
                #os.remove(item)

        video.release()
        cv2.destroyAllWindows()









        print('video is all read')
        break

