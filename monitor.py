from ivpdb import *
import requests
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








































