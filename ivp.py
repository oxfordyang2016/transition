from flask import Flask,request
app = Flask(__name__)
import requests
import json
from time import strftime 
import MySQLdb
import ast






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





@app.route('/')
def hello_world():
    return 'hello world'

@app.route('/api/v')
def version():
    versionofapi={'version':apiversion}
    return json.dumps(versionofapi)






#register ivp
#r=requests.post('http://192.168.201.142:50/ivps',json={'ip':'192.168.50.182','user':'yangming','addressofdevice':'shanghai','phone':'110'})
@app.route('/ivps',methods = ['POST', 'GET'])
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
    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user))



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
def registered():
    ivpid = request.args.get('ivpid')
    cursor.execute("select * from infoofivp where ivpid= "+"'"+str(ivpid)+"'")
    registeredinfo=getrow()
    print('hallo')
    return json.dumps(registeredinfo)



#look encoder info
#analysis which boads is  ready in ivp device according to ip

def readyboards(ip):
    '''
    request example
    requests.get('http://192.168.0.181/cgi-bin/boardcontroller.cgi?action=get&object=boardmap&id=0.8234045444577069')
    '''
    url='http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=boardmap'
    elegantresponse=ast.literal_eval(requests.get(url).text)
    #according to encoder/decoder list to decide which type is every board
    print elegantresponse
    return elegantresponse


#Being ready group ofsingle device 

@app.route('/ivp/readygroup')
def singledevicereadygroup():
    
    ivpid = request.args.get('ivpid')
    ip=paserip(str(ivpid))
    #print readyboards(str(ip)
    k=readyboards(str(ip))
    print k
    return json.dumps(k)
    


#look encoder info


#lookup decoder info













#lookup smip info
@app.route('/smip')
def getsmip():
    ivpid = request.args.get('ivpid')
    ip=paserip(str(ivpid))
    try:
        smipinfo0=requests.get('http://'+str(ip)+'/boardcontroller.cgi?action=get&object=slot6&key=channel_status&instanceID=0' ).json()
        smipinfo1=requests.get('http://'+str(ip)+'/boardcontroller.cgi?action=get&object=slot6&key=ip_profile&instanceID=0').json()
    except:
        smipinfo0=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=slot6&key=channel_status&instanceID=0' ).json()
        smipinfo1=requests.get('http://'+str(ip)+'/cgi-bin/boardcontroller.cgi?action=get&object=slot6&key=ip_profile&instanceID=0').json()
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
    ge={'Network setting':{'work mode':net1['ipmode'],'mask':net1['mask'],'gateway':net1['ge'],'ip':net1['ad']},'phy configuration':{'an':net1["an"],'phy speed':net1['spddup'],'status':net1['s']}}
    infogroup={'smip-stream':stream,'smipgessetting':ge}    
    return json.dumps(infogroup)







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

