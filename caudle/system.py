############################
# File: caudle/system.py
# Written by: John J Caine
# Description: This is the system module handling all system-level settings
############################

import MySQLdb as mdb
from datetime import datetime
import time

class DBConnection(object):
    
    def __init__(self):
        pass
    
    def connect(self, user, password, host, database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        
        try:
            db = mdb.connect(
                    host=self.host,
                    user=self.user,
                    passwd=self.password,
                    db=self.database
                )
            cur = db.cursor()
        except mdb.Error, e:
            print  "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
            exit(1)
        return cur
    
class Source(object):
    def __init__(self):
        pass
    
    gameURLSource = "http://scores.espn.go.com/ncb/scoreboard?confId=50&date="
    rosterURLSource = "http://espn.go.com/mens-college-basketball/teams"
    
class SysConfig(object):
    
    def __init__(self):
        pass
    
    logFile = "logs/log.txt"
    
class Utility(object):
    def __init__(self):
        pass
    
    def timeStamp(self):
        ts = time.time()
        return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    
    def convertToInches(self, feet, inches):
        return (feet * 12) + inches
    
    def convertToFeet(self, inches):
        feet = inches / 12
        inches = inches % 12
        return feet, inches
    
    def get_schooldict(self, cur):
        schoolDict = {}
        cur.execute('SELECT teamname, teamid FROM team')
        for row in cur.fetchall():
            schoolDict[row[0]] = row[1]
        return schoolDict