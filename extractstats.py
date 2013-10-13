'''
Created on Aug 20, 2013

@author: jcaine
'''
import bs4
import urllib 
import MySQLdb 
import datetime
from bs4 import BeautifulSoup

#connect to db
db = MySQLdb.connect(host = "localhost",
                     user = "root",
                     passwd = "password",
                     db = "ncbstats")
#create cursor
cur = db.cursor()

#returns a the date of the game, the time of the game, 
#and a list with each player, and their game stats
def get_score_data(url):
    """Return gameId (str), date (date), time (time), location (str), 
    homeTeam (int), awayTeam (int), homeFinal (int), awayFinal (int), 
    and playerRows (list) for a given espn game URL.    
    """
    
    #initialize variables
    rows = []
    playerRows = []
    html = urllib.urlopen(url).read()
    schoolDict = get_schooldict()
    homeTeam = -1
    awayTeam = -1
    gameId = url[url.find('=')+1:]

    #main data extraction block
    if html:
        print "Getting the score data for game " + gameId
        
        soup = BeautifulSoup(html)
        
        #game date
        dateElement = soup.find(class_="game-time-location").find("p")
        datetime = dateElement.get_text()
        time = (datetime[:datetime.find(',')]).encode('utf-8')
        time = convert_time(time)
        date = (datetime[datetime.find(',')+2:]).encode('utf-8')
        
        #game location
        locationElement = dateElement.find_next('p')
        location = locationElement.get_text()
        
        #score data
        awayFinalElement = soup.find(class_="ts")
        awayFinal = awayFinalElement.get_text()
        
        homeFinalElement = awayFinalElement.find_next(class_="ts")
        homeFinal = homeFinalElement.get_text()

        #find school1
        school1 = soup.find(id="my-players-table").find("th")
        school1Name = (school1.get_text()).encode('utf-8')
        #replace school name with schoolid
        if schoolDict.has_key(school1Name):
            awayTeam = int(schoolDict[school1Name])
        else:
            print school1Name + " doesn't exist... adding it..."
            add_school(school1Name)
            schoolDict = get_schooldict()
            awayTeam = int(schoolDict[school1Name])
        
        #Find school1 starter stats
        starters = soup.find(id="my-players-table").find("tbody")
        for row in starters.find_all('tr'):
            rows.append([awayTeam] + [val.text.encode('utf-8') for val in row.find_all('td')] + [1])

        #find school1 bench stats
        bench = starters.next_sibling.next_sibling
        for row in bench.find_all('tr'):
            rows.append([awayTeam] + [val.text.encode('utf-8') for val in row.find_all('td')] + [0])
        
        #find school2
        school2 = soup.find(id="my-players-table").find("thead")
        school2 = school2.find_next_sibling("thead").find_next_sibling("thead").find_next_sibling("thead")
        school2Name = (school2.find("th").get_text()).encode('utf-8')
        #replace school name with schoolid... if the school doesn't exist, create it
        if schoolDict.has_key(school2Name):
            homeTeam = int(schoolDict[school2Name])
        else:
            print school2Name + "doesn't exist... adding it..."
            add_school(school2Name)
            schoolDict = get_schooldict()
            homeTeam = int(schoolDict[school2Name])
        
        #Find school2 starter stats
        starters = school2.find_next_sibling("tbody")
        for row in starters.find_all('tr'):
            rows.append([homeTeam] + [val.text.encode('utf-8') for val in row.find_all('td')] + [1])
        
        #find school2 bench stats
        bench = starters.next_sibling.next_sibling
        for row in bench.find_all('tr'):
            rows.append([homeTeam] + [val.text.encode('utf-8') for val in row.find_all('td')] + [0])
            

    #remove the bad rows
    for row in rows:
        if (row and row[0] > -1 and len(row) > 10):
            playerRows.append([gameId] + row)

    #make player position its own field and replace dashes in stats
    for row in playerRows:
        #split player and position
        playerpos = row[2]
        commaIndex = playerpos.rfind(',')
        if commaIndex == -1:
            position = 'N'
            player = playerpos
        else:
            position = playerpos[commaIndex+2:]
            player = playerpos[:commaIndex]
        row[2] = player
        row.insert(3, position)
        
        #handle cases where minutes doesn't exist for the line score... make the minutes -1 for that player
        if '-' in row[4]:
            row.insert(4, -1)
        
        #make 'of' stats two fields
        i = 5
        while i < 11:
            s1 = row[i][:row[i].index('-')]
            s2 = row[i][row[i].index('-')+1:]
            if s1 == '':
                s1 = 0
            if s2 == '':
                s2 = 0
            row.pop(i)
            row.insert(i, s1)
            row.insert(i+1, s2)
            i = i+2
            
        

    return gameId, date, time, location, homeTeam, awayTeam, homeFinal, awayFinal, playerRows

#returns a list of every schools team page url
def get_school_urls():
    """Return list of team page URLs for all college basketball teams on ESPN."""
    #initialize variables
    url = 'http://espn.go.com/mens-college-basketball/teams'
    html = urllib.urlopen(url)
    soup = BeautifulSoup(html)
    
    #get all the school URLs
    schoolurls = []
    schoolTags = soup.find_all(class_='bi')
    for row in schoolTags:
        schoolurls.append(row.get('href'))
   
    return schoolurls

#returns a list of every school roster url
def get_roster_urls():
    """Return list of roster URLs for all schools on ESPN.com"""
    #initialize variables
    url = 'http://espn.go.com/mens-college-basketball/teams'
    html = urllib.urlopen(url)
    soup = BeautifulSoup(html)
    
    print "Getting all of the roster URLs..."
    
    #get all the roster URLs
    rosterurls = []
    for link in soup.find_all('a'):
            href = link.get('href')
            if href <> None and "roster?" in href:
                rosterurls.append([('http://espn.go.com' + href).encode('utf-8')])
    
    print "Done!"
    
    return rosterurls

#returns a list of each player and their vitals
def get_roster(url):
    """Return a list of players from the url provided."""
    html = urllib.urlopen(url)
    soup = BeautifulSoup(html)
    playerRow = []
    schoolDict = get_schooldict()
    
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
        row[0] = int(schoolDict[row[0]])
        
    print "Done!"
    return playerRow
    

def get_schools(self, urls):
    """Returns a list with all of the schools and conferences"""
    schools = []
    for url in urls:
        print "Opening " + url
        html = urllib.urlopen(url)
        soup = BeautifulSoup(html)
        
        teamNameElement = soup.find(class_="sub-brand-title")
        teamName = teamNameElement.get_text()
        
        conferenceNameElement = soup.find(class_="sub-title")
        conferenceName = conferenceNameElement.get_text()
        
        schools.append([conferenceName] + [teamName])
        
    return schools

def get_box_score_urls(beginDate, endDate):
    """Returns all of the box score URLs for a given date range from ESPN.com"""
    print "Getting the box score URLs..."
    urls = []
    oneDay = datetime.timedelta(days=1)
    
    #get the box score urls for the date rance
    while beginDate <= endDate:

        gameDate = str(beginDate)[:4] + str(beginDate)[5:7] + str(beginDate)[8:]
        url = 'http://scores.espn.go.com/ncb/scoreboard?date=' + gameDate + '&confId=50'
        html = urllib.urlopen(url)
        soup = BeautifulSoup(html)
        

        for link in soup.find_all('a'):
            href = link.get('href')
            if href <> None and "boxscore?" in href:
                urls.append([('http://scores.espn.go.com' + href).encode('utf-8')])
        
        beginDate = beginDate + oneDay
    
    return urls
      

def get_schooldict():
    """Return dictionary of schools and their teamid from the ncbstats database"""
    schoolDict = {}
    cur.execute('SELECT teamname, teamid FROM team')
    for row in cur.fetchall():
        schoolDict[row[0]] = row[1]
    return schoolDict

#returns a player's id number
def get_playerid(playerName, teamid):
    """Returns an integer of a playerid from the ncbstats database 
    for a given player's name and teamid.
    """
    #build player dictionary
    playerid = -1
    cur.execute("""SELECT playerid FROM player WHERE name = %s AND teamid = %s;""", (playerName, teamid))
    for row in cur.fetchall():
        playerid = int(row[0])
    if playerid == -1:
        firstInitial = playerName[:1]
        lastName = playerName[playerName.index(' '):]
        cur.execute("""SELECT * FROM player WHERE name LIKE %s and teamid = %s;""", (firstInitial + '%' + lastName, teamid))
        playerCount = 0
        for row in cur.fetchall():
            playerid = int(row[0])
            playerCount =+ 1
        if playerCount == 1:
            return playerid
        else:
            return -1
    else:
        return playerid
    
     
     
def insert_players(roster):
    """Inserts players into the ncbstats database"""
    for row in roster:
        cur.execute(
                """INSERT INTO player 
                    (teamid, number, name, position, height, weight, class, hometown) 
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
                    )
        db.commit()


def insert_game_data(startDate, endDate):
    """Inserts game data into the ncbstats database for a given date range."""
    gameCount = 0
    startDate = datetime.date(int(startDate[:4]), int(startDate[4:6]), int(startDate[6:]))
    endDate = datetime.date(int(endDate[:4]), int(endDate[4:6]), int(endDate[6:]))
    
    boxscoreurls = get_box_score_urls(startDate, endDate)
    
    for url in boxscoreurls:
        (gameId, date, time, location, homeTeam, awayTeam, homeFinal, awayFinal, playerRows) = get_score_data(url[0])
        if does_game_exist(gameId) == True:
            print "Warning: gameid " + gameId + " already exists! Skipping this game."
        else:
            #insert data into game table
            cur.execute("""INSERT INTO gamedata (gameid, hometeamid, awayteamid, date, starttime, location, hometotal, awaytotal) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s); """, (gameId, homeTeam, awayTeam, convert_date(date), time, location, homeFinal, awayFinal ))
            db.commit()
            
            #replace player name with playerid and insert the data into the database
            for player in playerRows:
                player.append(int(get_playerid(player[2], player[1])))
                if player[20] > -1: 
                    cur.execute("""
                                INSERT INTO scoredata
                                (gameid, playerid, starter, min, fgm, fga, tpm, tpa, ftm, fta, oreb, reb, ast, stl, blk, tos, pf, pts)
                                VALUES
                                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                """, (player[0], 
                                       int(player[20]), 
                                       int(player[19]), 
                                       int(player[4]), 
                                       int(player[5]), 
                                       int(player[6]), 
                                       int(player[7]), 
                                       int(player[8]), 
                                       int(player[9]), 
                                       int(player[10]), 
                                       int(player[11]), 
                                       int(player[12]), 
                                       int(player[13]), 
                                       int(player[14]), 
                                       int(player[15]), 
                                       int(player[16]), 
                                       int(player[17]), 
                                       int(player[18]) ))
                    db.commit()
                else:
                    #player doesn't exist... insert them into the player table
                    cur.execute("""
                                INSERT INTO player
                                (name, position, teamid)
                                VALUES
                                (%s, %s, %s)
                                """, (player[2], player[3][:1], player[1]))
                    db.commit()
                    
                    #then add their line score
                    player[20] = int(get_playerid(player[2], player[1]))
                    cur.execute("""
                                INSERT INTO scoredata
                                (gameid, playerid, starter, min, fgm, fga, tpm, tpa, ftm, fta, oreb, reb, ast, stl, blk, tos, pf, pts)
                                VALUES
                                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                                """, (player[0], 
                                       int(player[20]), 
                                       int(player[19]), 
                                       int(player[4]), 
                                       int(player[5]), 
                                       int(player[6]), 
                                       int(player[7]), 
                                       int(player[8]), 
                                       int(player[9]), 
                                       int(player[10]), 
                                       int(player[11]), 
                                       int(player[12]), 
                                       int(player[13]), 
                                       int(player[14]), 
                                       int(player[15]), 
                                       int(player[16]), 
                                       int(player[17]), 
                                       int(player[18]) ))
                    db.commit()

            gameCount +=1
            print "Successfully added data for game id: " + str(gameId) + ". Successfully added " + str(gameCount) + " games."

def add_school(schoolName):
    """Adds a school to the ncbstats database."""
    cur.execute("""INSERT INTO team (teamname, conferenceid) VALUES (%s, %s); """, (schoolName, -1) )

def does_game_exist(gameId):
    """Checks to see if a game exists in the ncbstats database and returns a bool."""
    rowCount = 0
    cur.execute("""SELECT COUNT(*) FROM gamedata WHERE gameid = %s """, (gameId))
    for row in cur.fetchall():
        rowCount = int(row[0])
    if rowCount > 0:
        return True
    else:
        return False

def convert_date(fullDate):
    """Returns a string of the given date in the format yy-mm-dd."""
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

def convert_time(time):
    """Converts time to 24-hr clock."""
    hours = time[:time.index(':')]
    minutes = time[time.index(':')+1:time.index(' ')]
    if 'PM' in time:
        hours = int(hours) + 12
    return str(hours) + ':' + minutes
