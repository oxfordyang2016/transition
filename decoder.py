from colors import red, green, blue,yellow
from flask import Flask,request
app = Flask(__name__)
import requests,json,ast,redis
from time import strftime 
from  ivpdb import *



#board group
allencodergroup=['7','8','9','10','11','17','19','25','34' ,'38','39' ]
alldecodergroup=['6','13','14','20','21','30']
tmp='7 8  9 10 11 17 19 25 34 38 39 6 13 14 20 21 30'
neededencodergroup=['10']
neededdecodergroup=['21']
apiversion='1.0'



      




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



#Being ready group ofsingle device 

#get single device work status
@app.route('/ivps/readygroup')
def singledevicereadygroup(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')
    ip=parserip(str(ivpid))
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
    
#lookup decoder info in single device   

@app.route('/ivps/decoders')
def singledevicedecoderinfo(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')
    ip=parserip(str(ivpid))
    #print readyboards(str(ip)
    info=readyboards(str(ip),neededencodergroup,neededdecodergroup)
    decoder=info[2]
    print  yellow('info is it===========================> '+str(info))
    print blue(str(decoder))
    decoderall={}
    alldecoder=[]
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
        avinfo={'position':i,'decoding status':decoding_status,'video info':videoinfo,'audioallinfo':audioinfo}
        alldecoder.append(avinfo)
    print info1,info2
    print type(decoderall)
    r.set(str(ivpid)+'decodergroup',avinfo)
    r.set(str(ivpid)+'decodersstatus',alldecoder)
    return json.dumps(decoderall)
    #return json.dumps(avinfo)
    '''
    info1=requests.get('http://192.168.0.181/cig-bin/boardcontroller.cgi?action=get&object='+str(encoder[0])+'&key=status').text
    #encoderall['info1']=info1
    return info1
    '''
def decodersource(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')
    ip=parserip(str(ivpid)) 
    '''
    http://192.168.0.181/cgi-bin/boardcontroller.cgi?action=get&object=router&slotid=slot4&slotport=sub_in_0&id=0.0852252272940579 
    '''
    ivpdecodergroup=['slot4']
    infogroup=[]
    for decoder in ivpdecodergroup:
        info=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=router&slotid='+str(decoder)+'&slotport=sub_in_0').text 
        print 'http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=router&slotid='+str(decoder)+'slotport=sub_in_0'
        finalinfo=ast.literal_eval(info)
        print red(str(finalinfo))
        try:
            print green('what happen=====================================>')
            lenoflist=len(finalinfo['Body']['Route_records'])
            for k in range(lenoflist):
                if 'slot6' in finalinfo['Body']['Route_records'][k]["src_id"]:
                    print red('i am ther-------------------->')
                    r.set(str(decoder)+'correspondingsmip',finalinfo['Body']['Route_records'][k]["src_port"])
                    r.set(str(ivpid)+finalinfo['Body']['Route_records'][k]["src_port"],decoder)
        except:
            r.set('ivpidencodersmip'+str(decoder),'')

for k in range(5):
    #singledeviceencoderinfo(ivpid='ivp201705170754')
    singledevicedecoderinfo(ivpid='ivp201705170754')
    decodersource(ivpid='ivp201705170754')
    #getsmip1(ivpid='ivp201705170754')





if __name__ == '__main__':
   app.run('0.0.0.0',100,debug='True')

