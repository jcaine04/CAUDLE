'''
Created on Oct 19, 2013

@author: johncaine
'''
import MySQLdb

class DatabaseManager(object):
    def __init__(self):
        try:
            self.db = MySQLdb.connect(
                                      host = "localhost",
                                      user = "root",
                                      passwd = "password",
                                      db = "ncbstats"
            )
        except:
            pass
        
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
        
db = DatabaseManager()
cur = db.query("SELECT name FROM player LIMIT 0,1")
print cur.fetchone()[0]

            