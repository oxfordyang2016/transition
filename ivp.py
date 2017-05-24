from colors import red, green, blue,yellow
from flask import Flask,request
app = Flask(__name__)
import requests
import json
from time import strftime 
import MySQLdb
import ast
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
redisallkey=[]





#board group
allencodergroup=['7','8','9','10','11','17','19','25','34' ,'38','39' ]
alldecodergroup=['6','13','14','20','21','30']
tmp='7 8  9 10 11 17 19 25 34 38 39 6 13 14 20 21 30'
neededencodergroup=['10']
neededdecodergroup=['21']
apiversion='1.0'
db=MySQLdb.connect(host='192.168.0.112', user='root', passwd='123456',db="ivp")
cursor=db.cursor()
#design solution
'''
0.clent sends registed info requests including ip,user,phone ect and server save the table in db
  and initiate the status all device  to be 'first registered'

1.we be-realtime change the status of all devices.the status written by a function ,the function need
to monitor all boards in the ivp and refresh the status every 10 seconds. 

2.in server  end.we refresh  the table.wow the server has 2 tables .a table is used to maintain the
  registered info ,another tables is used to log all device monitor info every 5 min

3.client sends request to server ,server tell clients all registered devices
   and the status of device then.(work/not work/)server give status ,the client send 
   requests to get detail info of the device(the requirements supplied by mr yao)

4.the standard ,my idea is the fewllowing:
  fecth the reuirements of every board.if can fecth ,i will give ok.and refresh the deivce registred
  table.clients send requests and we will fetch the device registered table.    

5.i will give the registered ivp hardware info.use serial number
6.i can give the link info (enccoder------smip-----smip-----decoder)
7.seach the info in ivp registred table to detect a  link.

'''









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





@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/api/v')
def version():
    versionofapi={'version':apiversion}
    return json.dumps(versionofapi)

@app.route('/api/errorcodes')
def errorcodes():
    errorcodelist=[{'0':'success'},{'11':'fail to query device status'},{'211':'errorcode api  internal error'}]
    try:
        return json.dumps({'errorcodelist':errorcodelist,'errorcode':0})
    except:
        return json.dumps({'errorcodelist':errorcodelist,'errorcode':211})
















#register ivp
#r=requests.post('http://192.168.201.142:50/ivps',json={'ip':'192.168.50.182','user':'yangming','addressofdevice':'shanghai','phone':'110'})
@app.route('/ivps',methods = ['POST'])
def register():
    if request.method == 'POST':
        #user = request.form['user']
        getjson=request.get_json(force=True)
        registeruser=getjson['user']
        registerip=getjson['ip']
        registeraddress=getjson['addressofdevice']
        registerphone=getjson['phone']        
        registerivpid='ivp'+strftime('%Y%m%d%H%M')
        ivpinfo={'user':registeruser,'ip':registerip,'ivpid':registerivpid,'addressofdevice':registeraddress,'phone':registerphone,'errorcode':1}
        
        #cursor.execute("INSERT INTO infoofivp  (ivpid,ip) VALUES" +"("+"'"+str(registerivpid)+"'"+","+"'"+str(registerip)+"'"+ ')' )
        cursor.execute("INSERT INTO infoofivp  (ivpid,ip,user,phone,addressofdevice) VALUES" +"("+"'"+str(registerivpid)+"'"+","+"'"+str(registerip)+"'"+","+"'"+str(registeruser)+"'"+","+"'"+str(registerphone)+"'"+","+"'"+str(registeraddress)+"'" +')')
        db.commit()


        return json.dumps(ivpinfo)
    #else:
        #user = request.args.get('nm')
        #return redirect(url_for('success',name = user))
        #return json.dumps({'errorcode':89})
        #workstatus()

#parser the ip of ivp device according to ivpid
def paserip(ivpid):
    cursor.execute("select * from infoofivp where ivpid= "+"'"+str(ivpid)+"'")
    registeredinfo=getrow()
    ip=registeredinfo['0']['ip']
    print(ip)
    return ip
      


#paserip('ivp201704120052')





#lookup registered ivp device
@app.route('/ivps/registered')
def registered(*args):
    ivpid = request.args.get('ivpid')
    print str(ivpid)+'ivp id is here'
    if ivpid!=None:
        cursor.execute("select * from infoofivp where ivpid= "+"'"+str(ivpid)+"'")
        print 'the line is  a bug---------------'
        registeredinfo=getrow()
    else:
        print 'i have enter except part--------------->'
        cursor.execute("select ivpid,devicestatus from infoofivp")
        print "select ivpid,devicestatus from infoofivp"
        registeredinfo=getrow()
        print registeredinfo
    
    #print('hallo')
    return json.dumps(registeredinfo)


#lookup all registered ivps
#i need to rethink that does it work with ivp device code?


@app.route('/ivps',methods=['GET'])
def workstatus(*args):
    ivpid = request.args.get('ivpid')
    if ivpid!=None:
        print('i am look for all status')
        return json.dumps(ast.literal_eval(r.get('ivp201705170754')))
    cursor.execute("select ivpid,devicestatus from infoofivp ")
    status=getrow()
    thenumberofivpid=len(status)
    statuslist=[]
    for k in range(thenumberofivpid):
        statuslist.append({str(status[str(k)]['ivpid']):status[str(k)]['devicestatus']})
    try:
        result={'statuslist':statuslist,'errorcode':0}
    except:
        #tmp error code =11
        result={'statuslist':'','errorcode':11}    
    return json.dumps(result)











#look encoder info
#analysis which boads is  ready in ivp device according to ip

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
        ip=paserip(str(k))
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





#allivpsboards()


#give positions info  to front

@app.route('/ivps/allpos1')
def getallpostions(*args):
    cursor.execute("select ip,ivpid,encodergroup,decodergroup from deviceworkingboard")
    allrow=getrow()
    item={}
    ivplist=[]
    for k in range(len(allrow)):
        try:
            ip=allrow[str(k)]['ip']
        except:
            ip=ast.literal_eval(allrow[str(k)]['ip'])
        try:
            ivpid=allrow[str(k)]['ivpid']
        except:
            ivpid=ast.literal_eval(allrow[str(k)]['ivpid'])
        try:
           print 'i m eval'
           encoder= ast.literal_eval(allrow[str(k)]['encodergroup']) 
           decoder= ast.literal_eval(allrow[str(k)]['decodergroup'])
        except:
           print red('i can not convert')
           encoder= allrow[str(k)]['encodergroup']
           decoder= allrow[str(k)]['decodergroup']
        item={'ivpid':ivpid,'encoder':encoder,'decoder':decoder,'ip':ip}
        ivplist.append(item)
    print ivplist
    result={'errorcode':'233','ivplist':ivplist}
    print red(str(result))
    
    #print allrow[str(i)]['encodergroup']
    
    #result={"ivplist":[{'ivpid':allrow[str(i)]['ivpid'],'encoder':allrow[str(i))]['encodergroup'],'decoder':allrow[str(i)]['decodergroup']}  for i in  range(len(allrow))],"errorcode":0}
    #print result
    '''
    result= json.dumps(result)
    test=result.replace('\\"',"\"")
    return test
    '''
    return json.dumps(result) 





#Being ready group ofsingle device 







#Being ready group ofsingle device 

#get single device work status
@app.route('/ivps/readygroup')
def singledevicereadygroup():
    
    ivpid = request.args.get('ivpid')
    ip=paserip(str(ivpid))
    #print readyboards(str(ip)
    info=readyboards(str(ip),allencodergroup,alldecodergroup)
    k=info[0] 
    all=k['Body']
    boardsgroup=[i for i in all.keys() if 'status' not in i]   
    encoder=[d for d in boardsgroup if all[str(d)] in allencodergroup]
    decoder=[d for d in boardsgroup if all[str(d)] in alldecodergroup]
    print encoder,decoder
    finalgroup={'encoder':encoder,'decoder':decoder}
    print yellow(str(finalgroup)) 
    return json.dumps(finalgroup)
    




    
 








'''
{'slot3': {'info1': u'{\n\t"Head":\t{\n\t\t"ErrorCode":\t"0",
\n\t\t"Message":\t"Success"\n\t},
\n\t"Body":\t{\n\t\t"status":\t"2",
\n\t\t"status_str":\t"Encoding",
\n\t\t"videoinfo":\t"255",\n\t\t"audioinfo":\t"0",
\n\t\t"videoinfo_str":\t"SDI-Unlocked",
\n\t\t"audioinfo_str0":\t"SDI-Lost",
\n\t\t"audioinfo_str1":\t"SDI-Lost",
\n\t\t"audioinfo_str2":\t"SDI-Lost",
\n\t\t"audioinfo_str3":\t"SDI-Lost"\n\t}\n}',






 'info2': u'{\n\t"Head":\t{\n\t\t"ErrorCode":\t"0",
 \n\t\t"Message":\t"Success"\n\t},
 \n\t"Body":\t{\n\t\t"BoardType":\t"HDELProfile",
 \n\t\t"profile_version":\t"3",\n\t\t"main_input_num":
 \t"1",\n\t\t"main_output_num":\t"1",
 \n\t\t"sub_input_num":\t"0",\n\t\t"sub_output_num":\t"2",
 \n\t\t"HDE_In1":\t"0",\n\t\t"videoPrivoder":\t"UNKNOWN",
 \n\t\t"videoSerName":\t"UNKNOWN",\n\t\t"biss":\t"0,0,0",
 \n\t\t"bitMode":\t"0",\n\t\t"audioParam0":\t"0,1,1,7,1F4,A,1",
 \n\t\t"audioParam1":\t"1,0,1,7,1F4,A,1",
 \n\t\t"audioParam2":\t"2,0,1,7,1F4,A,1",
 \n\t\t"audioParam3":\t"3,0,1,7,1F4,A,1",
 \n\t\t"audioALC0":\t"0,14,0,0,7D0,0",
 \n\t\t"audioALC1":\t"0,14,0,0,7D0,0",
 \n\t\t"audioALC2":\t"0,14,0,0,7D0,0",
 \n\t\t"audioALC3":\t"0,14,0,0,7D0,0",
 \n\t\t"videoParam":\t"1,2,0,5B8D80,3,28,1,0,1,0,0,0,0,1,1,0,1,20,2,0",
 \n\t\t"systemParam":\t"649DD0,1,40,410,420,421,422,423,400,410,64,23,64,3E8,0,1",
 \n\t\t"profile_crc":\t"4241230914"\n\t}\n}'}}
'''
#look all encoder info in single device//--------these requirements are implemented by mrs yao
@app.route('/ivps/encoders')
def singledeviceencoderinfo():
    ivpid = request.args.get('ivpid')
    ip=paserip(str(ivpid))
    #print readyboards(str(ip)
    info=readyboards(str(ip),neededencodergroup,neededdecodergroup)
    encoder=info[1]
    encoderall={}
    for i in encoder:
        print i
        encoder={}
        #http://192.168.0.181/cgi-bin/boardcontroller.cgi?action=get&object=slot3&key=status
        #print 'http://192.168.0.181/cig-bin/boardcontroller.cgi?action=get&object='+str(i)+'&key=status'
        info1=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object='+str(i)+'&key=status').text
        info2=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object='+str(i)+'&key=all').text
        selectedinfo1=ast.literal_eval(info1)
        selectedinfo2=ast.literal_eval(info2)
        print red(str(selectedinfo1))
        requirement1=selectedinfo1['Body']
        requirement2=selectedinfo2['Body']

        encoder_status={'encoding_status':requirement1['status_str'],'video input':requirement1['videoinfo_str'],'audio1to4input':{'audio1input':requirement1['audioinfo_str0'],'audio2input':requirement1['audioinfo_str1'],'audio3input':requirement1['audioinfo_str2'],'audio4input':requirement1['audioinfo_str3'], }}
        print(yellow(str(requirement2)))
        bitratesettingmode=requirement2['bitMode']

        programparameters={'service':requirement2['videoSerName'],'provider':[requirement2['videoPrivoder']],'biterate': [x.strip() for x in requirement2['systemParam'].split(',')][0]}
        vp=[x.strip() for x in requirement2['videoParam'].split(',')]
        videoparameters={'source':vp[0],'format':vp[1],'horizontal size':vp[2],'biterate':vp[3],'loss input':vp[-1]}
        ap1=[x.strip() for  x  in requirement2['audioParam0']]
        ap2=[x.strip() for  x  in requirement2['audioParam1']]
        ap3=[x.strip() for  x  in requirement2['audioParam2']]
        ap4=[x.strip() for  x  in requirement2['audioParam3']]
        ap=[ap1,ap2,ap3,ap4]
        
        audioparameters={}
        i=0
        for k in ap:
            i=i+1
            audioparameters['channel'+str(i)]={'source':k[0],'audio enable':k[1],'format':k[2],'loss of input':k[-2]}
        #spree
        bigbang={'encoder status':encoder_status,'encoder_setting':{'bitrate settingmode':bitratesettingmode,'videoParam':videoparameters,'programparameters':programparameters,'audioparameters':audioparameters}}

        encoder['info1']=info1
        encoder['info2']=info2
        encoderall[str(i)]=encoder
    #print info1,info2
    

    print"""

                             return info

           """
    #print type(encoderall)
    #print encoderall
    print red('i will print big bang')
    print bigbang
    #return json.dumps(encoderall)    
    return json.dumps(bigbang)
    '''
    info1=requests.get('http://192.168.0.181/cig-bin/boardcontroller.cgi?action=get&object='+str(encoder[0])+'&key=status').text
    #encoderall['info1']=info1
    return info1
    '''








#lookup decoder info in single device   

@app.route('/ivps/decoders')
def singledevicedecoderinfo(*args):
    ivpid = request.args.get('ivpid')
    ip=paserip(str(ivpid))
    #print readyboards(str(ip)
    info=readyboards(str(ip),neededencodergroup,neededdecodergroup)
    decoder=info[2]
    print  yellow('info is it===========================> '+str(info))
    print blue(str(decoder))
    decoderall={}
    for i in decoder:
        print i
        decoder={}
        #http://192.168.0.181/cgi-bin/boardcontroller.cgi?action=get&object=slot3&key=status
        print 'http://192.168.0.181/cig-bin/boardcontroller.cgi?action=get&object=slot'+str(i)+'&key=status'
        ins1='http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=slot'+str(i)+'&key=status'
        print blue(ins1)
        info1=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object='+str(i)+'&key=status').text

        info2=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object='+str(i)+'&key=avinfo&value=0').text
        info3=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object='+str(i)+'&key=avinfo&value=1').text
        decoder['info1']=info1
        decoder['info2']=info2
        decoder['info3']=info3
        #decoderall[str(i)]=decoder
        print yellow('info1------>'+str(info1))
        selectedinfo1=ast.literal_eval(info1)
        selectedinfo2=ast.literal_eval(info2)
        selectedinfo3=ast.literal_eval(info3)
        print red(str(selectedinfo1)) 
        requirement1=selectedinfo1['Body']
        requirement2=selectedinfo2['Body']
        requirement3=selectedinfo3['Body']['audinfo']
        decoding_status=requirement1['status_str']
        videoinfo={'format':requirement2['format'],'chroma':requirement2['chroma'],'biterate':requirement2['bitrate']}
        audioinfo={'audio1':requirement3[0],'audio2':requirement3[1],'audio3':requirement3[2],'audio4':requirement3[3]}
        avinfo={'decoding status':decoding_status,'video info':videoinfo,'audioallinfo':audioinfo}







    

    print info1,info2
    print type(decoderall)
    #return json.dumps(decoderall)
    return json.dumps(avinfo)
    '''
    info1=requests.get('http://192.168.0.181/cig-bin/boardcontroller.cgi?action=get&object='+str(encoder[0])+'&key=status').text
    #encoderall['info1']=info1
    return info1
    '''







@app.route('/ivps/allpos')
def allpos(*args):
    cursor.execute('select allposandtype.ivpid,allposandstatus.ip,u1status,d1status ,u2status,d2status,u3status,d3status,u1type,d1type,u2type,d2type,u3type,d3type from allposandstatus,allposandtype where allposandstatus.ivpid=allposandtype.ivpid')
    allpos=getrow()
    print allpos
    thenumberofivpid=len(allpos)
    allposlist=[]
    for k in range(thenumberofivpid):
        allposlist.append({"id":allpos[str(k)]['ivpid'],"ip":allpos[str(k)]['ip'],"slot_list":[
{"slot0":{'name':allpos[str(k)]['d1type'],'status':allpos[str(k)]['d1status']}},{"slot1":{'name':allpos[str(k)]['d2type'],'status':allpos[str(k)]['d2status']}},{"slot2":{'name':allpos[str(k)]['d3type'],'status':allpos[str(k)]['d3status']}},{"slot3":{'name':allpos[str(k)]['u1type'],'status':allpos[str(k)]['u1status']}},{"slot4":{'name':allpos[str(k)]['u2type'],'status':allpos[str(k)]['u2status']}},{"slot5":{'name':allpos[str(k)]['u3type'],'status':allpos[str(k)]['u3status']}}]})    



    result={'ivp_list':allposlist,'errorcode':0}
    return json.dumps(result)



























#lookup smip info
@app.route('/smip')
def getsmip(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')
    result=r.get(str(ivpid)+'smipinfo')
    finalresult=ast.literal_eval(result)     
    return json.dumps(finalresult)



if __name__ == '__main__':
   app.run('0.0.0.0',50,debug='True')

