############################
# File: caudle/system.py
# Written by: John J Caine
# Description: This is the system module handling all system-level settings
############################

import MySQLdb as mdb

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
            print "Error %d: %s" % (e.args[0],e.args[1]) 
            
        return cur