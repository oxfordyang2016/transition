from ivpdb import *
app = Flask(__name__)


neededencodergroup=['10']
neededdecodergroup=['21']

#Being ready group ofsingle device     
#look all encoder info in single device//--------these requirements are implemented by mrs yao
@app.route('/ivps/encoders')
def singledeviceencoderinfo(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')    
    ip=parserip(str(ivpid))
    #print readyboards(str(ip)
    info=readyboards(str(ip),neededencodergroup,neededdecodergroup)
    encoder=info[1]
    encoderall={}
    allencoder=[]
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

        encoder_status={'encoding_status':requirement1['status_str'],\
        'video input':requirement1['videoinfo_str'],\
        'audio1to4input':{'audio1input':requirement1['audioinfo_str0'],\
        'audio2input':requirement1['audioinfo_str1'],'audio3input':requirement1['audioinfo_str2'],\
        'audio4input':requirement1['audioinfo_str3'], }}
        


        #print(yellow(str(requirement2)))
        bitratesettingmode=requirement2['bitMode']

        programparameters={'service':requirement2['videoSerName'],\
        'provider':[requirement2['videoPrivoder']],\
        'biterate': [x.strip() for x in requirement2['systemParam'].split(',')][0]}
        
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

@app.route('/')
def test():
    return 'hello'






def allposfucks(ivpid='test'):
    ivpidgroup=allivpdevice()
    print ivpidgroup
    allivpboardsgroup=[]
    boardsgroup=['slot0','slot1','slot2','slot3','slot4','slot5','slot6']
    namedict={'10':'HDE','9':'HDE','21':'HDO','13':'DDO','28':'SMIP','52':'SMIP-C5'}
    for k in ivpidgroup:
        ip=parserip(str(k))
        url='http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=boardmap'
        try:
            response=ast.literal_eval(requests.get(url).text)
            slotgroup=response['Body']
            print type(slotgroup)
        except:
            response='no group info'
            slotgroup=''
        slots=[]
        print yellow(str(slotgroup))
        for slot in boardsgroup:
            try:
                slots.append({str(slot):{'name':namedict[str(slotgroup[str(slot)])],'status':slotgroup[str(slot)+'_status']}})
            except:
                #pass
                slots.append({str(slot):{'name':'','status':''}})

        print red(str(slots))
        allivpboardsgroup.append({'id':k,'ip':str(parserip(str(k))),'slot_list':slots})
   
    print(allivpboardsgroup)
    r.set('allivpboardsgroup',allivpboardsgroup)

















for k in range(100):
    for k in allivpdevice():
        #singledeviceencoderinfo(ivpid='ivp201705170754')
        #singledevicedecoderinfo(k)
        singledeviceencoderinfo(k)
        #singledevicedecoderinfo(ivpid='ivp201705170754')
        #getsmip1(ivpid='ivp201705170754')
        allposfucks()
        sleep(10)



if __name__ == '__main__':
   app.run('0.0.0.0',90,debug='True')

