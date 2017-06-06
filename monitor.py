from ivpdb import *
import requests,os
from colors import *
import ast

def geterror(ivpid):
    ip=parserip(ivpid)
    #http://192.168.0.181/cgi-bin/logmng.cgi?action=get&object=eventLog&key=log&logType=8&pageId=1&linesPerPage=f&logNotViewed=0&id=0.29722913455341105
    query='http://'+str(ip)+'/cgi-bin/logmng.cgi?action=get&object=eventLog&key=log&logType=8&pageId=1&linesPerPage=f&logNotViewed=0'
    result=ast.literal_eval(requests.get(query).text)
    return result



def getwarn(ivpid):
    ip=parserip(ivpid)
    #http://192.168.0.181/cgi-bin/logmng.cgi?action=get&object=eventLog&key=log&logType=4&pageId=1&linesPerPage=f&logNotViewed=0&id=0.8394339508798929 
    query='http://'+str(ip)+'/cgi-bin/logmng.cgi?action=get&object=eventLog&key=log&logType=4&pageId=1&linesPerPage=f&logNotViewed=0'
    result=ast.literal_eval(requests.get(query).text)
    return result



def getmainboardinfo(ivpid):
    #http://192.168.0.181/cgi-bin/system.cgi?action=get&object=status&key=all
    ip=parserip(ivpid)
    query='http://'+str(ip)+'/cgi-bin/system.cgi?action=get&object=status&key=all'
    result=ast.literal_eval(requests.get(query).text)
    return result






def check_ping(ivpid='test',ip='test'):
    if ivpid!='test':
        ip=parserip(ivpid)
    
    hostname = ip
    response = os.system("ping -c 1 " + hostname)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"

    return pingstatus





def pinghost(ivpid):
    hostname=parserip(ivpid)
    response = os.system("ping -c 1 " + hostname)

    #anthen check the response...
    if response == 0:
        print hostname, 'is up!'
        result='reachable'
    else:
        print hostname, 'is down!'
        result='unreachable'
    return result
    


