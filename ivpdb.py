import MySQLdb,redis,ast,requests
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
        deviceslist.append(alldevice[str(k)]['ivpid'])
    return deviceslist



def readyboards(ip,encodergroup,decodergroup):
    '''
    request example
    requests.get('http://192.168.0.181/cgi-bin/boardcontroller.cgi?action=get&object=boardmap&id=0.8234045444577069')
    '''
    url='http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=boardmap'
    elegantresponse=ast.literal_eval(requests.get(url).text)
    #according to encoder/decoder list to decide which type is every board
    print elegantresponse
    all=elegantresponse['Body']
    boardsgroup=[i for i in all.keys() if 'status' not in i]
    encoder=[d for d in boardsgroup if all[str(d)] in encodergroup]
    decoder=[d for d in boardsgroup if all[str(d)] in decodergroup]
    print encoder,str(decoder)
    return [elegantresponse,encoder,decoder]



#write all ivps borads to database;
def allivpsboards():
    cursor.execute('select ivpid from infoofivp')
    allivp=getrow()
    print(allivp)
    ivpidgroup=[allivp[i]['ivpid'] for i in allivp.keys()]
    print ivpidgroup
    #result0=readyboards(ip,allencodergroup,alldecodergroup)

    for k in ivpidgroup:
        ip=parserip(str(k))
        #result0=readyboards(str(ip),allencodergroup,alldecodergroup)
        try:
            print red('are you ok-------------')
            info=readyboards(str(ip),allencodergroup,alldecodergroup)
            tmp=info[0] 
            all=tmp['Body']
            boardsgroup=[i for i in all.keys() if 'status' not in i]
            encoder=[d for d in boardsgroup if all[str(d)] in allencodergroup]
            decoder=[d for d in boardsgroup if all[str(d)] in alldecodergroup]
            print encoder,decoder
            finalgroup={'encoder':encoder,'decoder':decoder}
            #encoder={k:'working' for k in encoder}
            #decoder={k:'working' for k in decoder}
            result1=['0',encoder,decoder]
           

        except:
            result1=['0','','']
        print red('insert into deviceworkingboard (ivpid,encodergroup,decodergroup) values'+"("+"'"+str(k)+"'"+","+"'"+json.dumps(result1[1])+"'"+","+"'"+json.dumps(result1[2])+"'"+")")
        cursor.execute('insert into deviceworkingboard (ip,ivpid,encodergroup,decodergroup) values'+"("+"'"+str(ip)+"'"+","+"'"+k+"'"+","+"'"+json.dumps(result1[1])+"'"+","+"'"+json.dumps(result1[2])+"'"+")")        
        #cursor.execute("INSERT INTO infoofivp  (ivpid,ip,user,phone,addressofdevice) VALUES" +"("+"'"+str(registerivpid)+"'"+","+"'"+str(registerip)+"'"+","+"'"+str(registeruser)+"'"+","+"'"+str(registerphone)+"'"+","+"'"+str(registeraddress)+"'" +')')

    
