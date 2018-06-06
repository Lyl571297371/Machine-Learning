#-*-coding:utf-8-*-

# 7.py说明  将测试图片删除
import os
def del_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".png"):
                os.remove(os.path.join(root, name))
                print("Delete File: " + os.path.join(root, name))
# test
if __name__ == "__main__":
    path = "./test_img"
    del_files(path)