from colors import *
def dividingline():
    print yellow('<===============================Dividing line=============================================>')

pos="""

                                                                 

                                                                 /\
                                                                /  \ 
                                                               /    \
                                                               \    / 
                                                                \  /
                                                                 \/





"""

pos1="""                                                                   
                                                                          ||
                                                                          ||
                                                                          || 
                                                                          ||
                                                                          ||
                                                                          ||
                                                                          vv
                                                                          88
                                                                          vv  

"""
def position():
    print(green(pos1))
    


def yangshow(var):
    linenumber1=linenumber()
    print(yellow('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  '+str(var)+'  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'))



from inspect import currentframe

def linenumber():
    cf = currentframe()
    print yellow(str(cf.f_back.f_lineno))
    return 'linenumber->'+str(cf.f_back.f_lineno)


