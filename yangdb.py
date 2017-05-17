import MySQLdb
db=''
cursor=''
#can connect mysql and mariadb
def connectmysql(host,user,passwd,db):
	db=MySQLdb.connect(host, user, passwd,db)
	cursor=db.cursor()

def execute(sql):
    cursor.execute(str(sql))


#get row accoring to the above sql
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


#return the qury result of fianl.
def ultimatesql(host,user,passwd,db,sql):
	connectmysql(host,user,passwd,db)
	execute(sql)
	result=getrow()
	return result



