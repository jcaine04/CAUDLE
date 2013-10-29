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
    
    #returns a list of each player and their vitals
    #return order: teamid, number, name, position, height (inches), weight, class, hometown
    def getRoster(self, url):
        """Return a list of players from the url provided."""
        html = urllib2.urlopen(url)
        soup = BeautifulSoup(html)
        playerRow = []

        print "Getting roster at " + str(url)

        teamName = soup.find(class_="sub-brand-title")
        teamName = (teamName.get_text()).encode('utf-8')

        for row in soup.find_all(class_="oddrow"):
            playerRow.append([teamName] + [val.text.encode('utf-8') for val in row.find_all('td')])
        for row in soup.find_all(class_="evenrow"):
            playerRow.append([teamName] + [val.text.encode('utf-8') for val in row.find_all('td')])

        for row in playerRow:
            rowCount = 0
            #convert height to inches
            if len(row) == 8:
                height = row[4]
                feet = int(height[:1])
                inches = int(height[2:])
                height = (feet*12) + inches
                row.pop(4)
                row.insert(4, height)
            else:
                print "Skipped row because row was not the correct length:"
                print row
                playerRow.pop(rowCount)
                rowCount -= 1
            rowCount += 1
            #replace school name with schoolid
            row[0] = int(self.teamDict([row[0]]))

        print "Done!"
        return playerRow

    
    def getBoxScoreUrls(self, beginDate, endDate):
        pass
    
    def teamDict(self, teamName):
        try:
            cur = self.db.query("""SELECT teamname, teamid FROM team WHERE teamname = %s""" % teamName)
        except self.db.Error, e:
            print "There was an error... %s: %s" % (e.args[0], e.args[1])
            return None
        else:
            teamid = cur.fetchone()[0]
            if teamid:
                self.addTeam(teamName)
            else:
                self.teamDict(teamName)
    
    def playerDict(self, playerName, schoolId, season=None):
        if not season:
            season = self.sys.currentSeason
        try:
            cur = self.db.query("""SELECT playerid
                                FROM player
                                WHERE playername = %s
                                AND season = %s""" % playerName, season
            )
        except self.db.Error, e:
            print "There was an error... %s: %s" % (e.args[0], e.args[1])
            return None
        else:
            teamid = cur.fetchone()[0]
            if teamid:
                self.addPlayer(playerName)
            else:
                self.teamDict(playerName)
    
    def addPlayer(self, playerList):
        pass
    
    def addTeam(self, teamName, conferenceId=-1):
        pass
    
    def addRoster(self, teamId, playerList):
        pass