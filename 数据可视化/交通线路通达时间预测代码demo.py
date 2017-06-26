#encoding=utf-8
import re
import sys
import pandas as pd
import math

#作者：Yin
#交通线路通达时间预测竞赛 示例程序

#经纬度计算距离2点间的距离
def calcu_distance(lon1,lat1,lon2,lat2):
      dx = lon1 - lon2
      dy = lat1 - lat2
      b = (lat1 + lat2) / 2.0;
      Lx = (dx/57.2958) * 6371004.0* math.cos(b/57.2958)
      Ly = 6371004.0 * (dy/57.2958)
      return math.sqrt(Lx * Lx + Ly * Ly)

#用pandas读入测试数据文件，并给每列起个名字
df1 = pd.read_csv("./data/predPaths_test.txt", header=None, names=["pathid","taxi_id","lat","lon","busy","dtime"])

distance = []
path_id =""
i=0
#算相邻2点的距离
for row in df1.itertuples(index=False):
    if path_id != row[0]:
        path_id = row[0]
        distance.append(0)
        lon1=row[3]
        lat1=row[2]
    else:
        x=calcu_distance(lon1=lon1,lat1=lat1,lon2=row[3],lat2=row[2])
        distance.append(x)
        lon1=row[3]
        lat1=row[2]

    if i%10000 == 0:
        sys.stdout.flush()
        sys.stdout.write("#")
    i=i+1
 
df1["distance"]=distance

#汇总计算每个path的里程
df2=df1.groupby('pathid').agg({'distance':'sum'})
df2=df2.reset_index()


#给距离做个线性变换，得到一个估计的时间
df2['distance']=df2['distance']*0.01+1300
df2.columns=['pathid','time']

#输出结果文件
df2.to_csv("out.csv",index=False)
#LB: 0.23***5 