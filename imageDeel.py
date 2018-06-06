#-*-coding:utf-8-*-

import numpy as np
from PIL import Image
#定义的标准
#Standard size 标准大小
N = 32
#Gray threshold 灰度阈值
color = 150
#设置变宽
side_width = 3

def JudgeEdge(img, length, flag, size):
    # JudgeEdge of Picture判断图片切割的边界
    for i in range(length):
        #Row or Column 判断是行是列
        if flag == 0:
            #Positive sequence 正序判断该行是否有手写数字
            line1 = img[i, img[i,:]<color]
            #Negative sequence 倒序判断该行是否有手写数字
            line2 = img[length-1-i, img[length-1-i,:]<color]
        else:
            line1 = img[img[:,i]<color, i]
            line2 = img[img[:,length-1-i]<color,length-1-i]
        #If edge, recode serial number 若有手写数字，即到达边界，记录下行
        if len(line1)>=1 and size[0]==-1:
            if i-side_width<=0:
                size[0] = 0
            else:
                size[0] = i-side_width
        if len(line2)>=1 and size[1]==-1:
            if length-1 <= length-1-i+side_width:
                size[1] = length-1
            else:
                size[1] = length-1-i+side_width
        #If get the both of edge, break 若上下边界都得到，则跳出
        if size[0]!=-1 and size[1]!=-1:
            break
    return size

def CutPicture(img):
    #CurPicture   切割图象
    # 去噪处理
    img[img>color] = 255
    img[img<=color] = 0
    #初始化新大小
    size = []
    #图片的行数
    length = len(img)
    #图片的列数
    width = len(img[0,:])
    #计算新大小
    size.append(JudgeEdge(img, length, 0, [-1, -1]))
    size.append(JudgeEdge(img, width, 1, [-1, -1]))
    size = np.array(size).reshape(4)
    # 裁剪后的图片
    new_img = img[size[0]:size[1]+1, size[2]:size[3]+1]
    return new_img

def StretchPicture(img):
    #StretchPicture  拉伸图像
    # 获取图片的宽高
    img_with = len(img[0, :])
    img_height = len(img)
    # 创建一张图片
    image = Image.new("L", (img_with, img_height))
    #矩阵转化成图片
    #循环图片的高和宽，分别吧图片的灰度值添加到对应的图片的位置上，这个时候创建图片秤成功
    for i in range(img_height):
        lineStr = img[i]
        for j in range(img_with):
            colorValue = int(lineStr[j])
            image.putpixel((j, i), int(colorValue))

    # 图片创建成功后对图片进行缩放 成 32x32的标准图片
    new_image = image.convert("L").resize((32, 32))

    #再将图片转换成功矩阵
    data = np.array(new_image)

    # 将黑色像素设置为1
    data[data==0] = 1
    # 将白色像素设置为0
    data[data==255] = 0
    return data