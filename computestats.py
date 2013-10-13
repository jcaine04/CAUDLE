'''
Created on Sep 2, 2013

@author: johncaine
'''


def calc_game_possessions(db, gameid):
    """Return possessions for the game provided"""
    
    cur = db.cursor()
    
    #get the home and away teams
    teamSQL = """
            SELECT hometeamid, awayteamid
            FROM gamedata
            WHERE gameid = %s
            """
            
    homeTeam = 0
    awayTeam = 0
    cur.execute(teamSQL, gameid)
    for row in cur.fetchall():
        homeTeam = row[0]
        awayTeam = row[1]
        
    #SQL to get stats needed to calc possessions
    possSQL = """
            SELECT
                s.fga, 
                s.oreb, 
                s.tos, 
                s.fta
            FROM scoredata s
            JOIN player p
            ON s.playerid = p.playerid
            WHERE s.gameid = %s and p.teamid = %s
            """
    #calculate home possessions
    homeFGATotal = 0
    homeOREBTotal = 0
    homeTOTotal = 0
    homeFTATotal = 0
    cur.execute(possSQL, (gameid, homeTeam))
    for row in cur.fetchall():
        homeFGATotal += int(row[0])
        homeOREBTotal += int(row[1])
        homeTOTotal += int(row[2])
        homeFTATotal += int(row[3])
        
    homePossessions = ((homeFGATotal - homeOREBTotal) + homeTOTotal) + (0.4 * homeFTATotal)
    
    #calculate away possessions
    awayFGATotal = 0
    awayOREBTotal = 0
    awayTOTotal = 0
    awayFTATotal = 0
    cur.execute(possSQL, (gameid, awayTeam))
    for row in cur.fetchall():
        awayFGATotal += int(row[0])
        awayOREBTotal += int(row[1])
        awayTOTotal += int(row[2])
        awayFTATotal += int(row[3])
        
    awayPossessions = ((awayFGATotal - awayOREBTotal) + awayTOTotal) + (0.4 * awayFTATotal)
        
    return (homePossessions + awayPossessions) / 2.0
    
def insert_possessions(db, gameid, poss):
    """Insert the provided possessions for the provided gameid"""
    cur = db.cursor()
    sql = """
        UPDATE gamedata
        SET poss = %s
        WHERE gameid = %s
        """
    cur.execute(sql, (poss, gameid))
    db.commit()

def update_all_null_possessions(db):
    """Update any games where possessions have not been calculated"""
    cur = db.cursor()
    
    #get all games where possession is null
    sql = """
        SELECT gameid
        FROM gamedata
        WHERE poss IS NULL
        """
    count = 0
    cur.execute(sql)
    for row in cur.fetchall():
        possessions = calc_game_possessions(db, row[0])
        insert_possessions(db, row[0], possessions)
        count +=1
    print "Updated " + str(count) + "games."