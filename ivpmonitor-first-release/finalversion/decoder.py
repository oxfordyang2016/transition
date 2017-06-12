
from  ivpdb import *
app = Flask(__name__)

@app.route('/')
def test():
    return 'hello'




neededencodergroup=['10']
neededdecodergroup=['21']

@app.route('/ivps/decoders')
def singledevicedecoderinfo(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')
    ip=parserip(str(ivpid))
    #print readyboards(str(ip)
    info=readyboards(str(ip),neededencodergroup,neededdecodergroup)
    decoder=info[2]
    #print  yellow('info is it===========================> '+str(info))
    #print blue(str(decoder))
    decoderall={}
    alldecoder=[]
    for i in decoder:
        print i
        decoder={}
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
    

    r.set(str(ivpid)+'decodergroup',decoder)
    r.set(str(ivpid)+'decodersstatus',alldecoder)
    return json.dumps(decoderall)






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




'''
for k in range(5):
    #singledeviceencoderinfo(ivpid='ivp201705170754')
    singledevicedecoderinfo(ivpid='ivp201705170754')
    decodersource(ivpid='ivp201705170754')
    #getsmip1(ivpid='ivp201705170754')
'''

for k in range(100):
    for ivp in allivpdevice():
        singledevicedecoderinfo(ivp)
        decodersource(ivp)
        sleep(10)



if __name__ == '__main__':
   app.run('0.0.0.0',100,debug='True')

