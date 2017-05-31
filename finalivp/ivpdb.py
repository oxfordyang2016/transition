import MySQLdb,redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
db=MySQLdb.connect(host='192.168.0.112', user='root', passwd='123456',db="ivp")
cursor=db.cursor()
#define a function to get table row info and write it to dict
def getrow():
    # commit your changes
    db.commit()
    tabledict={}
    numrows = int(cursor.rowcount)
    num_fields = len(cursor.description)
    field_names = [i[0] for i in cursor.description]
    for x in range(0,numrows):
        row = cursor.fetchone()
        #print(row)
        tmpdict={}
        for k in range(0,len(row)):
            #print str(field_names[k])+"                 |---------------------------->"+str(row[k]) 
            tmpdict[str(field_names[k])]=str(row[k])
        tabledict[str(x)]=tmpdict
    return tabledict


#parser the ip of ivp device according to ivpid
def parserip(ivpid):
    cursor.execute("select * from infoofivp where ivpid= "+"'"+str(ivpid)+"'")
    registeredinfo=getrow()
    ip=registeredinfo['0']['ip']
    print(ip)
    return ip

#parser all ivpid in table
def allivpdevice():
    cursor.execute("select ivpid from infoofivp")
    alldevice=getrow()
    thenumberofdevices=len(alldevice)
    deviceslist=[]
    for k in  range(thenumberofdevices):
        deviceslist.append(alldevice[str(k+1)]['ivpid'])
    return deviceslist


