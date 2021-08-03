import numpy as np
import cv2
#读取一张图片
size = (2400,1080)
print(size)
#完成写入对象的创建，第一个参数是合成之后的视频的名称，第二个参数是可以使用的编码器，第三个参数是帧率即每秒钟展示多少张图片，第四个参数是图片大小信息
videowrite = cv2.VideoWriter(r'E:\pedestrian_volume\xiaochijie.mp4',-1,5,size)
#20是帧数，size是图片尺寸
img_array=[]
for filename in [r'E:\pedestrian_volume\image\mp4_{0}.jpg'.format(i) for i in range(1,572)]:
    img = cv2.imread(filename)
    if img is None:
        print(filename + " is error!")
        continue
        img_array.append(img)
        for i in range(1,572):
            videowrite.write(img_array[i])
            print('end!')

import cv2
#读取一张图片
img = cv2.imread('E:\pedestrian_volume\image1\mp4_1.jpg')
#获取当前图片的信息
imgInfo = img.shape
fourcc = cv2.VideoWriter_fourcc(*'XVID')
size = (imgInfo[1],imgInfo[0])
print(size)
#完成写入对象的创建，第一个参数是合成之后的视频的名称，第二个参数是可以使用的编码器，第三个参数是帧率即每秒钟展示多少张图片，第四个参数是图片大小信息
videowrite = cv2.VideoWriter('E:\pedestrian_volume/xiaochijie1.avi',fourcc,5,size,True)
for i in range(1,572):
    fileName = 'E:\pedestrian_volume\image1/'+'mp4_' + str(i) + '.jpg'
    img = cv2.imread(fileName)
    #写入参数，参数是图片编码之前的数据
    videowrite.write(img)
print('end!')
