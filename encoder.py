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
def singledevicereadygroup(ivpid='test'):
    if ivpid=='test':
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
def singledeviceencoderinfo(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')    
    ip=paserip(str(ivpid))
    #print readyboards(str(ip)
    info=readyboards(str(ip),neededencodergroup,neededdecodergroup)
    encoder=info[1]
    encoderall={}
    alldecoder=[]
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
        bigbang={'position':i,'encoder status':encoder_status,'encoder_setting':{'bitrate settingmode':bitratesettingmode,'videoParam':videoparameters,'programparameters':programparameters,'audioparameters':audioparameters}}
        allencoder.append(bigbang)
        encoder['info1']=info1
        encoder['info2']=info2
        encoderall[str(i)]=encoder
    #print type(encoderall)
    #print encoderall
    print red('i will print big bang')
    print bigbang
    r.set(str(ivpid)+'encodergroup',str(bigbang))
    r.set(str(ivpid)+'encodersstatus',str(bigbang))
    #return json.dumps(encoderall)    
    return json.dumps(bigbang)
    '''
    info1=requests.get('http://192.168.0.181/cig-bin/boardcontroller.cgi?action=get&object='+str(encoder[0])+'&key=status').text
    #encoderall['info1']=info1
    return info1
    '''


for k in range(100):
    singledeviceencoderinfo(ivpid='ivp201705170754')
    #singledevicedecoderinfo(ivpid='ivp201705170754')
    #getsmip1(ivpid='ivp201705170754')





if __name__ == '__main__':
   app.run('0.0.0.0',90,debug='True')

