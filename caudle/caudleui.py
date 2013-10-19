'''
Created on Oct 19, 2013

@author: johncaine
'''
    
class MainMenu(object):
    
    def __init__(self):
        pass
    
    def display(self):
        #main menu
        print "CAUDLE v0.1..."
        print "Select an option:"
        print "1) Extract stats"
        print "2) Calculate stats"
        print "3) Exit" 
        
        option = raw_input("> ")
        if option == "1":
            return "extract_stats"
        if option == "2":
            return "calculate_stats"
        if option == "3":
            print "Good bye!"
            exit(1)
        else:
            print "Sorry, that is not a valid option"
        return "main_menu"

class ExtractStatsMenu(object):
    def __init__(self):
        pass
    
    def display(self):
        print "Extract Stats Menu"
        exit(1)

class CalculateStatsMenu(object):
    def __init__(self):
        pass
    
    def display(self):
        print "Calculate Stats Menu"
        exit(1)
    
class Menu(object):
        
    menus = {
        "main_menu": MainMenu(),
        "extract_stats": ExtractStatsMenu(),
        "calculate_stats": CalculateStatsMenu()
        }
    
    def __init__(self, menu):
        self.menu = menu
        
    def nextMenu(self, menu):
        return Menu.menus.get(menu)
        
    def startMenu(self):
        return self.nextMenu(self.menu)