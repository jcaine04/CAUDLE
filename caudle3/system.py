import MySQLdb
import os
import time

from datetime import datetime


class DatabaseManager(object):
    
    def __init__(self):
        try:
            self.db = MySQLdb.connect()(
                                        host = "localhost",
                                        user = "root",
                                        passwd = "password",
                                        db = "ncbstats"
            )
        except:
            print "Unable to connect to database."
            exit(1)
        else:
            self.cur = self.db.cursor()
            
    def query(self, arg):
        try:
            self.cur.execute(arg)
        except MySQLdb.Error, e:
            print "There was an error... %s: %s" % (e.args[0], e.args[1])
            exit(1)
        else:    
            return self.cur
    
    def dbinsert(self, arg):
        try:
            self.cur.execute(arg)
        except MySQLdb.Error, e:
            print "There was an error... %s: %s" % (e.args[0], e.args[1])
            exit(1)
        else:
            self.db.commit()
            return True

    def __del__(self):
        self.cur.close()

        
class Utilities(object):
    
    def __init__(self):
        pass
    
    def getTimeStamp(self):
        ts = time.time()
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    def convertDate(self, fullDate):
        monthDict = {
                     'January' : '01',
                     'February' : '02',
                     'March' : '03',
                     'April' : '04',
                     'May' : '05',
                     'June' : '06',
                     'July' : '07',
                     'August' : '08',
                     'September' : '09',
                     'October' : '10',
                     'November' : '11',
                     'December' : '12'
        }
        
        month = monthDict[fullDate[:fullDate.index(' ')]]
        day = fullDate[fullDate.index(' ')+1:fullDate.index(',')]
        if int(day) < 10:
            day = '0' + day
        year = fullDate[fullDate.index(',')+2:]
        
        return year + '-' + month + '-' + day
    
    def convertTime(self, time):
        hours = time[:time.index(':')]
        minutes = time[time.index(':')+1:time.index(' ')]
        if 'PM' in time:
            hours = int(hours) + 12
        return str(hours) + ':' + minutes
    
 
class SysConfig(object):       
     
    currentSeason = ''
    gameURLSource = "http://scores.espn.go.com/ncb/scoreboard?confId=50&date="
    rosterURLSource = "http://espn.go.com/mens-college-basketball/teams"
    logFile = 'logs/log.txt'

    def __init__(self):
        self.db = DatabaseManager()
        q = self.db.query("""SELECT currentseason FROM sysconfig""")
        currentSeason = q.fetchone()[0]