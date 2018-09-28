import _thread
from math import log
from numpy import zeros
from random import randint,uniform
import matplotlib.pyplot as plt
import time
AntinaAngle = 120
AntinaRadius = 1000
GirdWidth = 50
K1 = 130
K2 = 70
K3 = 1
K4 = 1
K5 = 1
K6 = 1
K7 = 1
ClutterLoss = 1
d =  0.1#km,distance between bs and ms
AntinaHeight = 0.002
Hms = 1#m,height of ms abrove ground
Heff = 1
diffractionloss = 1
BuildingHeight = 0.008  #
n = 10      #BS scope
bigsize = 100  #whole gird
WeakCovergeValue = 90
OverCoverValue = 70

def PassLoss(d,AntinaHeight,BuildingHeight):
    D = pow((pow(d,2) + pow((AntinaHeight+BuildingHeight),2)),0.5)
    return K1 + K2*log(D,10) + K3*Hms + K4*log(Hms,10) + K5*log(Heff,10) + K6*log(Heff,10)*log(D,10) + K7*(diffractionloss) + ClutterLoss

def showMat(mat):
    for x in range(len(mat)):
        print(mat[x])
        print("\n")

def CalABsMatrix(AntinaHeight,BuildingHeight):
    center = (n-1)/2
    data = zeros((21,21))
    for i in range(n):
        for j in range(n):
            distance = pow((pow(0.05*(center - i),2) + pow(0.05*(center - j),2)),0.5)
            data[i][j] = int(PassLoss(distance,AntinaHeight,BuildingHeight))
    return data

def ToBigMatrix(smlMat,x,y,DirectionAngel):
    bigMat = zeros((200,200))
    for i in range(n):
        for j in range(n):
            bigMat[i+x][j+y] = smlMat[i][j]
    return bigMat

def generateRandowDistributeBS(numOfBS):
    Fields = []
    for i in range(numOfBS):
        x = randint(0,179)
        y = randint(0,179)
        AntinaAngle = randint(0,360)
        BuildingHeight = uniform(0.001,0.04)
        AntinaHeight = uniform(0.001,0.01)
        Fields.append(ToBigMatrix(CalABsMatrix(AntinaHeight,BuildingHeight),x,y,360))
    return Fields

# 1.  方向天线，覆盖范围400~600m之间（设置每一个天线参数）
# 2.  给出你实际的天线参数及其覆盖参数的示例
# 3.  区域范围改成5kmx5km, 栅格50x50 m^2
# 4.  计算时间。
def function():
    pass
if __name__ == '__main__':
    starttime = time.time()
    BSnums = [100,150,200,250,300,350,400,450,500,550,600]
    BSnums = [600]
    BSnumsWeakPctge = []
    BSnumsOverPctge = []
    NeededTime = []
    YTime = []
    totalTime = 0
    for BSnum in BSnums:
        FieldsStrenth = generateRandowDistributeBS(BSnum)
        # zzz = (FieldsStrenth[9])
        MatForResult = zeros((bigsize,bigsize))
        for i in range(bigsize):
            for j in range(bigsize):
                over3 = 0
                numOflow = 0
                for x in range(BSnum):
                    if ((FieldsStrenth[x][i][j] == 0.) or (FieldsStrenth[x][i][j] > WeakCovergeValue)):   #判定弱覆盖
                        numOflow += 1 
                    if abs(FieldsStrenth[x][i][j]) > 0.0001:  #计算过覆盖
                        if FieldsStrenth[x][i][j] < OverCoverValue:
                            over3 += 1
                if over3 > 3:
                    MatForResult[i][j] = 2
                if numOflow == BSnum:
                    MatForResult[i][j] = 1
        numOf1 = 0
        numOf2 = 0
        # showMat(MatForResult)   
        for i in range(bigsize):
            for j in range(bigsize):
                if MatForResult[i][j] == 1:
                    numOf1 += 1
                if MatForResult[i][j] == 2:
                    numOf2 += 1
        # print(numOf1)
        allGird = bigsize*bigsize
        WeakCoveragePercentage = float(numOf1/allGird)
        OverCoveragePercentage = float(numOf2/allGird)
        print("基站个数：" + str(BSnum))
        print("弱覆盖率：" + str(numOf1) + "/" + str(allGird),end="->")
        print(WeakCoveragePercentage)
        print("过覆盖率：" + str(numOf2) + "/" + str(allGird),end="->")
        print(OverCoveragePercentage)
        TimeSpent = time.time() - starttime
        totalTime += TimeSpent
        print("用时：" + str(int(TimeSpent)) + "s\n")
        BSnumsWeakPctge.append(WeakCoveragePercentage)
        BSnumsOverPctge.append(OverCoveragePercentage)
        YTime.append(TimeSpent)
    cc = []
    for x in BSnums:
        cc.append(x*3)
    print("本次一共用时：" + str(int(TimeSpent)) + "s\n")
    plt.figure()
    plt.plot(BSnums,BSnumsWeakPctge,label="WeakCoverage")
    plt.plot(BSnums,BSnumsOverPctge,label="OverCoverage")
    plt.xlabel("Num of BS")
    plt.ylabel("Percentage(100%)")
    plt.title("Tendency")
    plt.legend(loc = "best")
    plt.show()
    
    plt.figure()
    plt.plot(BSnums,BSnumsOverPctge)
    plt.xlabel("Num of BS")
    plt.ylabel("Time(s)")
    plt.title("BSnumsOverPctge")
    plt.legend(loc = "best")
    plt.show()

    plt.figure()
    plt.plot(BSnums,YTime)
    plt.xlabel("Num of BS")
    plt.ylabel("Time(s)")
    plt.title("Time consumption")
    plt.legend(loc = "best")
    plt.show()