'''
Created on Oct 19, 2013

@author: johncaine
'''

from system import DBConnection
import caudleui

class Main(object):
    
    def __init__(self, db, menu):
        self.db = db
        self.menu = menu
    
    def run(self):
        currentMenu = self.menu.startMenu()
        
        while True:
            print "\n----------"
            nextMenuName = currentMenu.display()
            currentMenu = self.menu.nextMenu(nextMenuName)
            

#establish db object
db = DBConnection()
#establish the main connection and cursor
cur = db.connect('root', 'password', 'localhost', 'ncbstats')
#set the first menu
menu = caudleui.Menu("main_menu")
#initialize the program
prog = Main(cur, menu)
#run the program
prog.run()