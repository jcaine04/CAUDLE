'''
Created on Oct 19, 2013

@author: johncaine
'''
import os
import sys
from system import Utility
from extractstats import TeamsExtract
from system import DBConnection


#establish db object
db = DBConnection()
#establish the main connection and cursor
cur = db.connect('root', 'password', 'localhost', 'ncbstats')
u = Utility()
t = TeamsExtract(cur)
r = t.getRosterURLs()
for i in r:
    print t.get_roster(i)