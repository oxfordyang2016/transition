from colors import *
from flask import Flask,request
app = Flask(__name__)
import requests,json,ast
from time import strftime 
from ivpdb import *


#board group
allencodergroup=['7','8','9','10','11','17','19','25','34' ,'38','39' ]
alldecodergroup=['6','13','14','20','21','30']
tmp='7 8  9 10 11 17 19 25 34 38 39 6 13 14 20 21 30'
neededencodergroup=['10']
neededdecodergroup=['21']
apiversion='1.0'


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
        ivpinfo={'user':registeruser,'ip':registerip,'ivpid':registerivpid,\
                 'addressofdevice':registeraddress,'phone':registerphone,'errorcode':1}
        cursor.execute("INSERT INTO infoofivp  (ivpid,ip,user,phone,addressofdevice) VALUES"\
                   +"("+"'"+str(registerivpid)+"'"+","+"'"+str(registerip)+"'"+","+"'"+\
                   str(registeruser)+"'"+","+"'"+str(registerphone)+"'"+","+"'"+\
                   str(registeraddress)+"'" +')')
        db.commit()
        return json.dumps(ivpinfo)

      

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
    
    return json.dumps(registeredinfo)




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



#get single device work status
@app.route('/ivps/readygroup')
def singledevicereadygroup():
    
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

@app.route('/ivps/encoders')
def singledeviceencoderinfo(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')
    result=r.get(str(ivpid)+'encodersstatus') 
    finalresult=ast.literal_eval(result)     
    return json.dumps(finalresult)



#lookup decoder info in single device   

@app.route('/ivps/decoders')
def singledevicedecoderinfo(ivpid='test'):
    if ivpid=='test':
        ivpid = request.args.get('ivpid')
    result=r.get(str(ivpid)+'decodersstatus') 
    finalresult=ast.literal_eval(result)     
    return json.dumps(finalresult)





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



@app.route('/stream')
def getalllink():
    linklist=[]
    ivpidlist=allivpdevice()    
    for k in ivpidlist:
        try:
            singleivplink=r.get(str(k)+'streamgroup'
            result=ast.literal_eval(singleivplink)
            linklist.append({k:result})
        except:
            linklist.append({k:'the ivpid has no stream'})
    
    finalresult={'errorcode':'200','linklist':linklist}
    
    return json.dumps(finalresult)




if __name__ == '__main__':
   app.run('0.0.0.0',50,debug='True')

