import system
from bs4 import BeautifulSoup
import urllib2

class DataExtraction(object):
    
    def __init__(self):
        self.db = system.DatabaseManager()
        self.util = system.Utilities()
        self.sys = system.SysConfig()
        
    def getGameData(self, url):
        pass
    
    def getTeamUrls(self):
        
        #initialize variables
        url = self.sys.rosterURLSource
        try:
            html = urllib2.urlopen(url)
        except:
            print "An error connecting to the URL occured. Please try again later."
            exit(1)

        soup = BeautifulSoup(html)
        
        #get all the school URLs
        schoolurls = []
        schoolTags = soup.find_all(class_='bi')
        for row in schoolTags:
            schoolurls.append(row.get('href'))
       
        return schoolurls
    
    def extractTeamRoster(self, url):
        pass
    
    def getBoxScoreUrls(self, beginDate, endDate):
        pass
    
    def teamDict(self, teamName):
        pass
    
    def playerDict(self, playerName, schoolId):
        pass
    
    def addPlayer(self, playerList):
        pass
    
    def addTeam(self, teamName, conferenceId=-1):
        pass
    
    def addRoster(self, teamId, playerList):
        pass