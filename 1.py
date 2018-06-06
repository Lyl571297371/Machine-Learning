#-*-coding:utf-8-*-

# 1.py说明   将训练图片准华为TXT文件


import os
from PIL import Image
import numpy as np
from imageDeel import *


def img2txt(img_path, txt_name):
    #将图像数据转化为TXT文件
    # img_path: 图像文件路径
    # txt_name: 输出txt文件路径
    # 将图片转换成灰度图片
    im = Image.open(img_path).convert('L')
    # im.save(txt_name)
    # 将图片转换成矩阵
    data = np.array(im)
    # # 裁剪图片
    new_data = CutPicture(data)
    # # # 缩放图片到标准大小
    new_data = StretchPicture(new_data)
    np.savetxt(txt_name, new_data, fmt='%d', delimiter='')


if __name__ == "__main__":
    # 获取指定目录下的所有文件
    fileList = os.listdir("./training_img/")
    # 遍历所有文件
    for file in fileList:
        # 获取文件名
        filename = file.split(".")[0]
        img2txt("./training_img/%s.png" % filename, "./knn-digits/trainingDigits/%s.txt" % filename)