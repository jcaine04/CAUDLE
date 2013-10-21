'''
Created on Oct 19, 2013

@author: johncaine
'''

from system import Source
from system import Utility
from caudlog import Logging
import urllib2
from bs4 import BeautifulSoup
import urllib

class TeamsExtract(object,):
    
    schoolDict = {}
    
    def __init__(self, db):
        self.db = db
        u = Utility()
        schoolDict = u.get_schooldict(db)
    
    def getRosterURLs(self):
        #initialize variables
        l = Logging()
        sourceURL = Source.rosterURLSource
        print "--------------------------------------"
        print "Attempting to get the roster URLs..."
        try:
            html = urllib2.urlopen(sourceURL)
        except urllib2.URLError as e:
            print "Extraction source unavailable or timed out. Please check your network connection."
            l.writeLog(e, 1)
            exit(1)
            
        soup = BeautifulSoup(html)
        
        #get all the roster URLs
        rosterurls = []
        try:
            for link in soup.find_all('a'):
                    href = link.get('href')
                    if href <> None and "roster?" in href:
                        rosterurls.append([('http://espn.go.com' + href)])
        except TypeError:
            print "An error occured. Please check the log file"
            msg = "Improper type returned None when parsing the page."
            Logging.writeLog(msg)
            exit(1)
        
        return rosterurls
    
    def get_roster(self, url):
        l = Logging()
        html = urllib.urlopen(url)
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
            #convert height to inches
            if len(row) == 8:
                height = row[4]
                feet = int(height[:1])
                inches = int(height[2:])
                height = (feet*12) + inches
                row.pop(4)
                row.insert(4, height)
            else:
                msg = "Warning: Skipped row because row was not the correct length: \n + Row: " + row
                l.writeLog(msg, 2)
                playerRow.pop(rowCount)
                
            #replace school name with schoolid
            row[0] = int(schoolDict[row[0]])
            
        
        return playerRow
    
    
    
    