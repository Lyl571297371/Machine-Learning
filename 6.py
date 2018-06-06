#-*-coding:utf-8-*-

# 6.py说明   将新增的TXT文件删除

import os
def del_files(path):
    for root, dirs, files in os.walk(path):
        for name in files:
            if name.endswith(".txt"):
                os.remove(os.path.join(root, name))
                print("Delete File: " + os.path.join(root, name))
# test
if __name__ == "__main__":
    path = "./knn-digits/newDigits"
    del_files(path)