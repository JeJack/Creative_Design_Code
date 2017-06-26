# encoding=utf-8
from pymongo import MongoClient
from pandas import Series,DataFrame
import pandas as pd
import math
import datetime
import matplotlib.pyplot as plt

f2init = open('E:/Creative_Design/TEST/around.csv','w')
f2init.close()

# 用pandas读入查询数据文件，并给每列起个名字，即测试数据
df2 = pd.read_csv('E:/Creative_Design/TEST/input.csv', header=None, names=["taxi_id2", "lat", "lon", "busy", "dtime"])

f = open("E:/Creative_Design/TEST/input.csv", "r")
f2 = open('E:/Creative_Design/TEST/around.csv','a')

client = MongoClient('127.0.0.1', 27017)
db_name = 'BigD'
db = client[db_name]
collection = db['taxiGPSB']
print(collection.find().count())
# query = {'ile': 5}
DL = 0.00005
while True:
    line = f.readline()
    LineStr=line.split(',')

    if line:
        FLAT = float(LineStr[2])
        FLON = float(LineStr[3])
        gtlat = FLAT - DL
        ltlat = FLAT + DL
        gtlon = FLON - DL
        ltlon = FLON + DL

        query = {"field1": {'$gt': gtlat, '$lt': ltlat},
                 "field2": {'$gt': gtlon, '$lt': ltlon}}  # ,"field2":{'$gt':104.090816,'$lt':104.090836}
        # query={"field4":{'$gt':'2014/8/28 12:19:25','$lt':'2014/8/28 13:19:25'}}
        cursor = collection.find(query)#.sort("ile", 1)
        # cursor.limit(100)
        for doc in cursor:
            f2.writelines(str(doc['ile']) + ',' + str(doc['field1']) + ',' + str(doc['field2']) + ',' + str(
                doc['field3']) + ',' + str(doc['field4']) + '\n')
            print(str(doc))

    else:
        break

f2.close()
f.close()

'''*************Taxi_ID和时间排序****************'''
import csv
data = csv.reader(open
                  ('E:/Creative_Design/TEST/around.csv'), delimiter=',')
sortedlist = sorted(data, key=lambda x: (int(x[0]),str(x[4])))
with open("E:/Creative_Design/FTEST.csv", "w") as fsort:
    fileWriter = csv.writer(fsort, delimiter=',')
    for row in sortedlist:
        fileWriter.writerow(row)
fsort.close()

'''****************计算时间 NO.1 *****************************'''

# 用pandas读入训练数据文件，并给每列起个名字，即测试数据周边的点
df1 = pd.read_csv('E:/Creative_Design/FTEST.csv', header=None, names=["taxi_id", "lat", "lon", "busy", "dtime"])


def pltshowX(ar):#显示图表
    plt.title("I'm a scatter diagram.")
    plt.xlim(xmax=500, xmin=0)
    plt.ylim(ymax=5, ymin=0)
    # ar=[1,2,3,4,5,6]
    plt.plot(ar, 'ro')
    plt.show()


# 经纬度计算距离2点间的距离
def calcu_distance(lon1, lat1, lon2, lat2):
    dx = lon1 - lon2
    dy = lat1 - lat2
    b = (lat1 + lat2) / 2.0;
    Lx = (dx / 57.2958) * 6371004.0 * math.cos(b / 57.2958)
    Ly = 6371004.0 * (dy / 57.2958)
    return math.sqrt(Lx * Lx + Ly * Ly)


distance = []
Dspeed=[]
Dpointlon=[]
Dpointlat=[]
taxi_id = ""
# 算相邻2点的距离
for row in df1.itertuples(index=False):
    if taxi_id != row[0]:
        taxi_id = row[0]
        distance.append(0)
        lon1 = row[2]
        lat1 = row[1]
        Cbusy=row[3]
        d1=datetime.datetime.strptime(str(row[4]),"%Y/%m/%d %H:%M:%S")
    else:
        x = calcu_distance(lon1=lon1, lat1=lat1, lon2=row[2], lat2=row[1])  #计算两个点之间的距离
        distance.append(x)
        lon1 = row[2]
        lat1 = row[1]
        DCbusy=Cbusy-row[3]
        Cbusy=row[3]
        d2 = datetime.datetime.strptime(str(row[4]), "%Y/%m/%d %H:%M:%S")
        dt=(d2-d1).seconds  #计算时间差
        if (dt > 0) and (dt < 120) and (x>20) and DCbusy==0:
            #如果两个点之间的时间间隔大于120s或者小于0s，时间是进过排序的
            # 则认为这两个点不是连续的，则没有价值。
            #如果连个点的距离不大于0，则认为车停在原地，那么这个数据就没有价值
            #如果两个点之间的距离小于20M，我认为车并没有行驶，此处可能是GPS定位上的误差。
            speedV = x / (d2 - d1).seconds
            if speedV>1.5 and  speedV <50 :#速度大于1m/s 才进入统计的速度
                Dspeed.append(speedV)
                Dpointlon.append(row[2])
                Dpointlat.append(row[1])

d1=DataFrame(Dpointlon,columns=['lon'])
d2=DataFrame(Dpointlat,columns=['lat'])
d3=DataFrame(Dspeed,columns=['speed'])
result=pd.concat([d1,d2,d3],axis=1)
result.to_csv("E:/Creative_Design/lonlatspeed2.csv", index=False)

V=sum(Dspeed)
if len(Dspeed)>0 :
    argvV=V/len(Dspeed)
    print ("平均速度为："+str(argvV))
'''************************查询文件坐标文件****************************'''

lon1=[]
lat1=[]
for row in df2.itertuples(index=False):
    lon1.append(row[2])
    lat1.append(row[1])

d1=DataFrame(lon1,columns=['lon'])
d2=DataFrame(lat1,columns=['lat'])
result=pd.concat([d1,d2],axis=1)
result.to_csv("E:/Creative_Design/lonlatTest.csv", index=False)

'''******************线性回归*************************'''

from sklearn.cross_validation import train_test_split  #这里是引用了交叉验证
from sklearn.linear_model import LinearRegression

data = pd.read_csv('E:/Creative_Design/lonlatspeed2.csv')#, header=None, names=[ "lon","lat","speed"]
data2 = pd.read_csv('E:/Creative_Design/lonlatTest.csv')
# f2 = open('E:/Creative_Design/D44.csv','w')
# visualize the relationship between the features and the response using scatterplots
# sns.pairplot(data, x_vars=["lon","lat" ], y_vars="speed", size=7, aspect=0.8)
# plt.show()#注意必须加上这一句，否则无法显示。

feature_cols=['lon','lat']
X=data[feature_cols]
X = data[['lon','lat']]

XTest=data2[['lon','lat']]

y = data['speed']
y = data.speed


X_train,X_test, y_train, y_test = train_test_split(X, y, random_state=1)

linreg = LinearRegression()
model=linreg.fit(X_train, y_train) # 进行training set和test set的fit，即是训练的过程

print ("预测模型的分数为：")
print linreg.score(X_test, y_test) # 获取模型的score值
print ("***************")
y_pred = linreg.predict(XTest)# 预测

Num_Speed=[] #存储速度的数组，测试文件除第一个点以外，每个点对应一个速度

for ii in y_pred:
    Num_Speed.append(float(ii))
print ("成功得到速度数组")

'''*******************得到速度数组************************'''

Sdistance = []
Dtime=[]
taxi_id2 = ""
i = 0
# 算相邻2点的距离
for row in df2.itertuples(index=False):
    if taxi_id2 != row[0]:
        taxi_id2 = row[0]
        Sdistance.append(0)
        lon1 = row[2]
        lat1 = row[1]
    else:
        x = calcu_distance(lon1=lon1, lat1=lat1, lon2=row[2], lat2=row[1])  #计算两个点之间的距离
        Sdistance.append(x)
        lon1 = row[2]
        lat1 = row[1]

        if x>0 and Num_Speed[i]>0:
            #两个点之间的距离需要大于0
            dt = x /Num_Speed[i] # Num_Speed[i] 为计算点的对应速度，此速度是线性回归模型中 点所对应的相应线性速度
            Dtime.append(dt)
    i = i + 1
#回归计算时间
FINtime=sum(Dtime)
print ("行驶路线的总时间为："+str(FINtime))#输出总时间
print("路线的总路程为："+str(sum(Sdistance)))
