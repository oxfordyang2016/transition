from colors import red, green, blue,yellow
from flask import Flask,request
import requests,json,ast
from  ivpdb  import *
from time import strftime 


app = Flask(__name__)
#board group
allencodergroup=['7','8','9','10','11','17','19','25','34' ,'38','39' ]
alldecodergroup=['6','13','14','20','21','30']
tmp='7 8  9 10 11 17 19 25 34 38 39 6 13 14 20 21 30'
neededencodergroup=['10']
neededdecodergroup=['21']

#single get info smip info function
'''
getsmipge('192.168,201',3)
'''
def getsmipge(ivpid,ge):
    ip=parserip(str(ivpid))
    smipinfo0=requests.get('http://'+str(ip)+\
        '/cgi-bin/boardcontroller.cgi?action=get&object=slot6&key=channel_status&instanceID='+str(ge)).text
    smipinfo1=requests.get('http://'+str(ip)+\
        '/cgi-bin/boardcontroller.cgi?action=get&object=slot6&key=ip_profile&instanceID='+str(ge)).text
    
    
    print(green('i  dnnot =====================understand what happen?'))    
    print yellow(smipinfo0)
    smipinfo0,smipinfo1=ast.literal_eval(smipinfo0),ast.literal_eval(smipinfo1)
    key0=smipinfo0['Body']['channel_status']
    print(yellow('i  dnnot =====================understand what happen?'))
    print key0
    print(green('i donnot understand what happen=========================>'))
    try:
        print('============================================>'+str(key0))
        st0=ast.literal_eval(key0)
        #st0=key0
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
        #st0=key0
        st1=ast.literal_eval(st0['o'])
        print(st1)
        st2=st1['orr']
        st3=st0
        st0=st1
   
    print(st0)
    print(red(str(type(st0))))    
    #you need to set the bufftime mechinism
    '''
    stream={'stream buffertime':"st0['bf']",'stream-setting':{'orr':st0['orr'],'rrar':st0['rrar'],
               'ip':st0['ipaddress'],'port':st0['ipport'],'setting-status':st0['msg'],
               'disconnect':st0['off_t'],'source':st0['source'],
       
                      'ge':st3['ge'],'mode':st0['status']}} 
    '''
    stream={'stream'+str(ge+1)+'settingip':st0['ipaddress']}
    r.set(str(ivpid)+'stream'+str(ge+1)+'settingip',st0['ipaddress'])
    #stream='i am test========================================================>'
    print(stream) 
    print "===========================vvvvvvvvvvvvvvvvvvvvvvvv============"+str(stream)    
    key1=smipinfo1['Body']
    '''
    {u'ip_profile': u'{"ad":"10.10.10.12","mac":"88:C2:55:8C:A0:90","mask":"255.255.255.0","ge":0,"dns":"10.10.10.1","ipmode":1,"io":0,"de":"","an":1,"spddup":3,"s":1,"bf":0}'
    '''
    #net0=ast.literal_eval(key1)
    net0=key1
    net1=ast.literal_eval(net0['ip_profile'])
    geinfo={'Network setting':{'work mode':net1['ipmode'],'mask':net1['mask'],'gateway':net1['ge'],'ip':net1['ad']},'phy configuration':{'an':net1["an"],'phy speed':net1['spddup'],'status':net1['s']}}
    r.set(str(ivpid)+'smipge'+str(ge+1)+'ip',net1['ad'])
    infogroup={'smip-stream'+str(ge):stream,'smipgessetting'+str(ge):geinfo}    
    print green(str(infogroup))
    return infogroup




#test yangming
#lookup smip info in function 
@app.route('/smipfunction')
def getsmip1(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')
    ip=parserip(str(ivpid))
    try:
        info1=getsmipge(ivpid,0)
    except:
        info1='the info of ge1 does not exist '
    try:
        info2=getsmipge(ivpid,1)
    except:
        info2='the info if ge2 does not exsit'

    try:    
        info3=getsmipge(ivpid,2)
    except:
        info3='the info of ge3 does not exsit'

    try:    
        info4=getsmipge(ivpid,3)
    except:
        info4='the info of ge4  does not exsit'

    allinfo={'info1':info1,'info2':info2,'info3':info3,'info4':info4}
    print red(str(allinfo))
    r.set(str(ivpid)+'smipinfo',allinfo)
    return json.dumps(allinfo)



@app.route('/link')
def getlink(ivpid='test'):
    if ivpid=='test':
        ivpid=request.args.get('ivpid')
    ip=parserip(str(ivpid))    
    stream1=requests.get('http://'+str(ip)+\
        '/cgi-bin/boardcontroller.cgi?action=get&object=router&slotid=slot6&slotport=SMIP_Out0').text
    stream2=requests.get('http://'+str(ip)+\
        '/cgi-bin/boardcontroller.cgi?action=get&object=router&slotid=slot6&slotport=SMIP_Out1').text
    stream3=requests.get('http://'+str(ip)+\
        '/cgi-bin/boardcontroller.cgi?action=get&object=router&slotid=slot6&slotport=SMIP_Out2').text
    stream4=requests.get('http://'+str(ip)+\
        '/cgi-bin/boardcontroller.cgi?action=get&object=router&slotid=slot6&slotport=SMIP_Out3').text
    st1=ast.literal_eval(stream1)
    st2=ast.literal_eval(stream2)
    st3=ast.literal_eval(stream3)
    st4=ast.literal_eval(stream4)
    try:
        if st1['Body']['Route_records']!=[]:
            r.set(str(ivpid)+'stream1source',\
                [st1['Body']['Route_records'][0]['src_id'],st1['Body']['Route_records'][0]['src_port']])
        r.set(str(ivpid)+'stream1',st1)
    except:
        r.set(str(ivpid)+'stream1','no')    
    try:
        if st2['Body']['Route_records']!=[]:
            r.set(str(ivpid)+'stream2source',\
                [st2['Body']['Route_records'][0]['src_id'],st2['Body']['Route_records'][0]['src_port']])        

        r.set(str(ivpid)+'stream2',st2)
    except:
        r.set(str(ivpid)+'stream2','no') 
    try:
        if st3['Body']['Route_records']!=[]:
            r.set(str(ivpid)+'stream3source',\
                [st3['Body']['Route_records'][0]['src_id'],st3['Body']['Route_records'][0]['src_port']])        
        r.set(str(ivpid)+'stream3',st3)
    except:
        r.set(str(ivpid)+'stream3','no') 
    try:
        r.set(str(ivpid)+'stream4',st4)
        if st4['Body']['Route_records']!=[]:
            r.set(st(ivpid)+'stream4source',[st4['Body']['Route_records'][0]['src_id'],st4['Body']['Route_records'][0]['src_port']])        
    except:
            r.set(str(ivpid)+'stream4','no') 
    return 'test'



#detect that a given ip in which ge of which ivp smip
def singleivpsmipipsettinggroup(ivpid):
    ipgroup=[]
    for ge in range(4):
        #print('ge is '+str(ge)+r.get(str(ivpid)+'smipge'+str(ge+1)+'ip')) 
        ipgroup.append(r.get(str(ivpid)+'smipge'+str(ge+1)+'ip'))
    print green(str(ipgroup))
    return ipgroup

def accrodingtoiptogetivp(ip):
    ivpgroup=['ivp201705170754']
    ivpsmipsettingipgroup={}
    for ivpid in ivpgroup:
        ivpsmipsettingipgroup[str(ivpid)]=singleivpsmipipsettinggroup(ivpid)
    #print yellow(str(ivpsmipsettingipgroup))
    for key in ivpsmipsettingipgroup:
        if str(ip) in ivpsmipsettingipgroup[str(key)]:
            #print red(str(ivpsmipsettingipgroup[str(key)]))
            #print 'the device is '+str(key)
            #get device id and ge position
            print('this device is '+str(key)+' ge is ge'+str(ivpsmipsettingipgroup[str(key)].index(str(ip))+1))
            #break
            return [key,str(str(ivpsmipsettingipgroup[str(key)].index(str(ip))+1))]



#what is wrong
def completelink(ivpid='test'):
    if ivpid=='test':
        ivpid=request.args.get('ivpid')
    singlesmipgroup=[{'stream'+str(k+1):r.get(str(ivpid)+'stream'+str(k+1)+'source')} for k in range(3) ]
    '''
    for k in range(4):
        singlesmipgroup.append(ast.literal_eval(r.get(str(ivpid)+'stream'+str(k+1)+'source')))
    for k in singlesmipgroup:
        if k!='':
            print('this stream encoder is the fellowing')
            print (k[0])
            print('this stream encoder type is')
            print(k[1])
            print('this stream distination rx smip is')
            print(r.get(stream1settingip))
    '''
    count=1
    singleivpdevicelink=[]
    for k in singlesmipgroup:
        print yellow('the curent device is '+str(ivpid)+'****')
        try:
            info=ast.literal_eval(k['stream'+str(count)])
        except:
            print('thers is a bug')
        if info!=None:
            print('this stream'+str(count)+' encoder is the fellowing')
            print(info[0])
            print('this stream encoder type is')
            print(info[1])
            print('this stream distination rx smip ip is')
            print(r.get('stream'+str(count)+'settingip'))
            
            ip=r.get('stream'+str(count)+'settingip')
            print('this stream desitination rx in fellowing deice')
            destination=accrodingtoiptogetivp(str(ip))
            coivp,coge=destination[0],destination[1]
            print('the destination ivp is '+str(coivp))
            print('this device corresponding ge is ge'+str(coge))
            print('the corresponding decoder position')
            print(r.get(str(coivp)+'SMIP_In'+str(int(coge)-1)))
            #print('')
        singleivpdevicelink.append({'stream'+str(count):{'encoder':info[0],\
            'encodertype':info[1],'destinationsmip':r.get('stream'+str(count)+'settingip'),\
            'destinationivp':str(coivp),'decoder':r.get(str(coivp)+'SMIP_In'+str(int(coge)-1))}})
        count+=1
    r.set(str(ivpid)+'streamgroup',singleivpdevicelink)






for k in range(1):
    getsmip1(ivpid='ivp201705170754')
    getlink(ivpid='ivp201705170754')
    completelink(ivpid='ivp201705170754')



if __name__ == '__main__':
   app.run('0.0.0.0',70,debug='True')

