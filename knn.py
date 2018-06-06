#-*-coding:utf-8-*-

import numpy
import operator
import os
import matplotlib.pyplot as plt
import shutil


# 将图像数据转换为（1，1024）向量
def img2vector(filename):
    returnVect = numpy.zeros((1, 1024))
    file = open(filename)
    for i in range(32):
        lineStr = file.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])
    return returnVect

# 添加新图片到训练库
def addTraningDigits(file_path_list):
    for path in file_path_list:
        shutil.copyfile(path['from'],path['to'])

# kNN分类器
def classifier(inX, dataSet, labels, k):
    #分类主题程序，计算欧氏距离，选择距离最小的K个，返回K个中出现频率最高的类别
    # inX: 测试样本向量
    # dataSet: dataSet是训练样本集，一行对应一个样本
    # labels: dataSet对应的标签向量为labels labels 中保存的是真实的值
    # k:k是所选的最近邻数目
    # 返回测试结果
    # shape[0]得出dataSet的行数，即样本个数
    dataSetSize = dataSet.shape[0]
    # tile(A,(m,n))将数组A作为元素构造m行n列的数组
    diffMat = numpy.tile(inX, (dataSetSize, 1)) - dataSet
    # 数组中每个元素平方
    sqDiffMat = diffMat ** 2
    # 求和
    sqDistances = sqDiffMat.sum(axis=1)
    # 开方
    distances = sqDistances ** 0.5
    # array.argsort()，按值升序排列后 得到每个元素的排序序号
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        # get(key,x)从字典中获取key对应的value，没有key的话返回0
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    # sorted()函数，按照第二个元素即value的次序逆向（reverse=True）排序
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# 测试手写数字识别代码
def handWritingClassTest(k):

    # 保存训练样本所代表的数字的真实值
    hwLabels = []

    # 使用一个字典保存每个数字的序号
    numCount = {}
    #将训练集中的所有样本转化成向量保存到数组中
    trainingFileList = os.listdir('knn-digits/trainingDigits')
    m = len(trainingFileList)
    trainingMat = numpy.zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        # 当前样本的序列号
        serialsNumStr = int(fileStr.split('_')[1])
        if int(serialsNumStr) > numCount.get(classNumStr,0):
            numCount[classNumStr] = int(serialsNumStr)
        # 保存真实值
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector("knn-digits/trainingDigits/%s" % fileNameStr)
        #将测试样本中的矩阵都取出来转化成矩阵，于训练集中的所有向量求欧氏距离，从而通过KNN算法判断测试样本所代表的数字的值
    testFileList = os.listdir('knn-digits/testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    # 设置一个空数组保存新的训练图片
    addTraning = []

    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        # 当前测试样本的数字值
        classNumStr = int(fileStr.split('_')[0])
        # 读取测试样本中的对应文件,并将其转换成1x1024的向量
        vectorTest = img2vector("knn-digits/testDigits/%s" % fileNameStr)
        # 将测试样本和训练集中的所有向量进行比对 识别出测试样本中的数字值
        result = classifier(vectorTest, trainingMat, hwLabels, k)
        print("分类结果是：%d, 真实结果是：%d" % (result, classNumStr))
        # 如果测试失败
        if result != classNumStr:
            # 错误量加一
            errorCount += 1.0
            # 从字典 numCount 获取当前数字出现的次数,如果没有获取到默认为0 然后加1
            numCount[classNumStr] = numCount.get(classNumStr, 0) + 1
            # 得到新增训练样本的序号
            nextNum = numCount[classNumStr]
            # 将测试样本作为训练样本保存到训练集中
            addTraning.append({
                "from": "knn-digits/testDigits/%s" % fileNameStr,
                "to": "knn-digits/newDigits/%s" % classNumStr + "_" + str(nextNum) + ".txt"
            })
            print("添加一张新训练图片 %s" % classNumStr + "_" + str(nextNum) + ".txt")
    # 添加图片
    addTraningDigits(addTraning)
    print("错误总数：%d" % errorCount)
    print("错误率：%f" % (errorCount / mTest))
    return errorCount


# 这里是为了测试取不同的k值，识别的效果如何
def selectK():
    x = list()
    y = list()
    for i in range(1, 5):
        x.append(int(i))
        y.append(int(handWritingClassTest(i)))
    plt.plot(x, y)
    plt.show()


