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
def paserip(ivpid):
    cursor.execute("select * from infoofivp where ivpid= "+"'"+str(ivpid)+"'")
    registeredinfo=getrow()
    ip=registeredinfo['0']['ip']
    print(ip)
    return ip
      




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










#single get info smip info function
'''
getsmipge('192.168,201',3)
'''
def getsmipge(ip,ge):
    try:
        smipinfo0=requests.get('http://'+str(ip)+'/boardcontroller.cgi?action=get&object=slot6&key=channel_status&instanceID='+str(ge) ).json()
        smipinfo1=requests.get('http://'+str(ip)+'/boardcontroller.cgi?action=get&object=slot6&key=ip_profile&instanceID='+str(ge)).json()
    except:
        smipinfo0=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=slot6&key=channel_status&instanceID='+str(ge) ).json()
        smipinfo1=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=slot6&key=ip_profile&instanceID='+str(ge)).json()
    print(smipinfo0)
    key0=smipinfo0['Body']['channel_status']
    
    print(key0)
    try:
        print('============================================>'+str(key0))
        st0=ast.literal_eval(key0)
        print('i will print---st0 in try-------------------------> '+str(st0))
        st1=ast.literal_eval(st0['i'])
        print('i am in st1 try ------------------------------------------------------------------->'+str(st1))
        st2=st1['orr']
        st3=st0
        st0=st1
        print('i have ===================arrive try end==============')          

   
    except:
        print("i am in except===========================================>")
        st0=(ast.literal_eval(key0))
        st1=ast.literal_eval(st0['o'])
        print(st1)
        st2=st1['orr']
        st3=st0
        st0=st1
   
    print(st0)
    
    #you need to set the bufftime mechinism
    stream={'stream buffertime':"st0['bf']",'stream-setting':{'orr':st0['orr'],'rrar':st0['rrar'],'ip':st0['ipaddress'],'port':st0['ipport'],'setting-status':st0['msg'],'disconnect':st0['off_t'],'ge':st3['ge'],'mode':st0['status']}} 
    key1=smipinfo1['Body']
    '''
    {u'ip_profile': u'{"ad":"10.10.10.12","mac":"88:C2:55:8C:A0:90","mask":"255.255.255.0","ge":0,"dns":"10.10.10.1","ipmode":1,"io":0,"de":"","an":1,"spddup":3,"s":1,"bf":0}'
    '''
    #net0=ast.literal_eval(key1)
    net0=key1
    net1=ast.literal_eval(net0['ip_profile'])
    geinfo={'Network setting':{'work mode':net1['ipmode'],'mask':net1['mask'],'gateway':net1['ge'],'ip':net1['ad']},'phy configuration':{'an':net1["an"],'phy speed':net1['spddup'],'status':net1['s']}}
    infogroup={'smip-stream'+str(ge):stream,'smipgessetting'+str(ge):geinfo}    
    return infogroup




#test yangming
#lookup smip info in function 
@app.route('/smipfunction')
def getsmip1():
    ivpid = request.args.get('ivpid')
    ip=paserip(str(ivpid))
    try:
        info1=getsmipge(ip,0)
    except:
        info1='the info of ge1 does not exist '
    try:
        info2=getsmipge(ip,1)
    except:
        info2='the info if ge2 does not exsit'

    try:    
        info3=getsmipge(ip,2)
    except:
        info3='the info of ge3 does not exsit'

    try:    
        info4=getsmipge(ip,3)
    except:
        info4='the info of ge4  does not exsit'

    allinfo={'info1':info1,'info2':info2,'info3':info3,'info4':info4}
    return json.dumps(allinfo)



if __name__ == '__main__':
   app.run('0.0.0.0',50,debug='True')

