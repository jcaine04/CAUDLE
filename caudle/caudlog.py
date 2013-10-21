'''
Created on Oct 19, 2013

@author: johncaine
'''
from system import SysConfig
from system import Utility


class Exceptions(object):
    '''
    classdocs
    '''
    def __init__(self):
        pass
        
class Logging(object):
    def __init__(self):
        pass
    
    def writeLog(self, msg, logType):
        s = SysConfig()
        u = Utility()
        
        logTypeDict = {
            1 : "Error",
            2 : "Warning",
            3 : "Message"
        }
        
        try:
            msg = str(msg)
        except:
            msg = "Couldn't convert error to string. Unknown error."
        try:
            f = open(s.logFile, 'wb')
            f.write(u.timeStamp() + ": " + logTypeDict.get(logType) + ": " +  msg + '\n')
            f.close
        except IOError:
            print "Couldn't write to the log file at " + str(s.logFile)
        