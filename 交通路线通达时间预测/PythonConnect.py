from pymongo import MongoClient

f2 = open('E:/Creative_Design/MongodbTestqiujie3.csv','a')

client = MongoClient('127.0.0.1', 27017)
db_name = 'BigD'
db = client[db_name]
collection = db['taxiGPSB']
print(collection.find().count())
# query = {'ile': 5}
DL=0.00005
FLAT=30.657726
FLON=104.090826
gtlat=FLAT-DL
ltlat=FLAT+DL
ltlon=FLON+DL

# query={"field1":{'$gt':gtlat,'$lt':ltlat},"field2":{'$gt':gtlon,'$lt':ltlon}}  #,"field2":{'$gt':104.090816,'$lt':104.090836}
query={"ile":2,"field4":{'$gt':'2014/8/28 21:00:00','$lt':'2014/8/28 21:30:00'}}
cursor = collection.find(query).sort("field4",1)
cursor.limit(100)
# for doc in cursor:
#     f2.writelines(str(doc['ile'])+','+str(doc['field1'])+','+str(doc['field2'])+','+str(doc['field3'])+','+str(doc['field4'])+'\n')
#     print(str(doc))
# f2.close()
for doc in cursor:
    f2.writelines(str(doc['ile'])+','+str(doc['field1'])+','+str(doc['field2'])+','+str(doc['field3'])+','+str(doc['field4'])+'\n')
    print(str(doc))
f2.close()
