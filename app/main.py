import urllib

from bs4 import BeautifulSoup

from app import app, db
from models import ConferenceModel, TeamModel, PlayerModel
from config import ESPN_TEAMS_URL, ESPN_ROOT, CURRENT_SEASON


class Game(object):
    pass


class Player(object):
    def __init__(self):
        self.utils = Utils()

    def add_player(self, team, player, season=CURRENT_SEASON, status=0):
        """
        Add a player the the database for a given team and player dictionary.
        Statuses:
            0: Uncommitted
            1: Committed
        """

        if not self.get_player(team, player['name']):
            p = PlayerModel(season=season,
                            name=player['name'],
                            number=player['number'],
                            position=player['position'],
                            height=player['height'],
                            weight=player['weight'],
                            academic_class=player['academic_class'],
                            hometown=player['hometown'],
                            status=status,
                            team=team)
            db.session.add(p)
            db.session.commit()

    def get_player(self, team, player_name):
        return PlayerModel.query.filter_by(name=player_name, team_id=team.id).first()


class Conference(object):

    def get_conference(self, name):
        """
        Queries for a conference object by conference name.
        """
        return ConferenceModel.query.filter_by(name=name).first()

    def add_conference(self, name):
        """
        Adds a conference to the database if the conference does not exist
        """
        if not self.get_conference(name):
            c = ConferenceModel(name=name)
            db.session.add(c)
            db.session.commit()


class Team(object):

    def __init__(self):
        self.utils = Utils()

    def extract_roster_urls(self):
        """
        Return a list of roster URLs for all schools.
        """
        soup = self.utils.make_soup(ESPN_TEAMS_URL)
        urls = []
        for link in soup.find_all('a'):
            urls.append(link.get('href'))
        return [url for url in urls if url and 'roster?' in url]

    def extract_conference_and_team_name(self, url):
        """
        Returns the conference name and the team name for the given url.
        """
        soup = self.utils.make_soup(ESPN_ROOT + url)
        if not soup:
            raise SoupException("Soup was empty for url %s" % (url))
        team_name_element = soup.find(class_="sub-brand-title")
        team_name = team_name_element.get_text()

        conference_name_element = soup.find(class_="sub-title")
        conference_name = conference_name_element.get_text()
        # Once the season has started, the conference is prefaced with
        # and conference position so we need to see if the string ' in '
        # exists so we can pull out the conference after it.
        in_position = conference_name.find(' in ')
        if in_position > -1:
            conference_name = conference_name[in_position + 4:]

        return conference_name, team_name

    def add_team(self, team_name, conference_name="Unknown"):
        """
        Adds a team to the database if that team does not exist.
        """
        conference = ConferenceModel.query.filter_by(name=conference_name).first()
        if not self.get_team(team_name):
            team = TeamModel(name=team_name, conference=conference)
            db.session.add(team)
            db.session.commit()

    def add_all_conferences_and_teams(self):
        """
        Extract all NCAA DI Men's Conferences Teams from stats source
        and add them to the database
        """
        c = Conference()
        urls = self.extract_roster_urls()
        for url in urls:
            conference_name, team_name = self.extract_conference_and_team_name(url)
            c.add_conference(conference_name)
            print team_name
            self.add_team(team_name, conference_name)

    def get_team(self, team_name):
        """
        Returns a team given a team name.
        """
        return TeamModel.query.filter_by(name=team_name).first()

    def extract_roster(self, url):
        """
        Returns a TeamModel object and a roster list for a given roster URL.
        """
        soup = self.utils.make_soup(ESPN_ROOT + url)
        if not soup:
            raise SoupException("Soup was empty for url")
        # team name is found at class "sub-brand-title"
        team_name = soup.find(class_="sub-brand-title").get_text()

        # The player table rows are defined by the classes "oddrow"
        # and "evenrow". Get the players and add them to the roster list.
        roster_list = []
        for row in soup.find_all(class_="oddrow"):
            roster_list.append([val.text.encode('utf-8') for val in row.find_all('td')])
        for row in soup.find_all(class_="evenrow"):
            roster_list.append([val.text.encode('utf-8') for val in row.find_all('td')])

        # Remove any bad rows
        roster_list = [player for player in roster_list if len(player) == 7]

        # Make the player into a dictionary so we have named attributes.
        roster = []
        for player in roster_list:
            roster.append(dict(
                        number=player[0].strip(),
                        name=player[1].strip(),
                        position=player[2].strip(),
                        height=self.utils.convert_to_inches(player[3][:1], player[3][2:]),
                        weight=player[4],
                        academic_class=player[5].strip(),
                        hometown=player[6].strip()))

        # get the TeamModel object for this team
        team_object = self.get_team(team_name)

        # if the team doesn't exist, create it and then get it
        if not team_object:
            self.add_team(team_name)
            team_object = self.get_team(team_name)

        return team_object, roster

    def add_roster(self, team, roster):
        """
        Adds a roster to the database for the given team and roster.
        """
        p = Player()
        for player in roster:
            try:
                p.add_player(team, player, status=1)
            except KeyError, e:
                print "There was a KeyError: %s." % (e)
                print team + " || " + player

    def add_all_rosters(self):
        """
        Extracts and adds all rosters from all teams from the stats source
        """
        roster_urls = self.extract_roster_urls()
        for url in roster_urls:
            team, roster = self.extract_roster(url)
            self.add_roster(team, roster)


class Utils(object):

    def make_soup(self, url):
        try:
            html = urllib.urlopen(url)
        except Exception, e:
            print "Error %s" % (e)
            return None
        return BeautifulSoup(html)

    def convert_to_inches(self, feet, inches=0):
        return (int(feet) * 12) + int(inches)

    def convert_to_feet(self, inches):
        feet = inches/12
        inches = inches % 12
        return feet, inches


class CaudleException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class SoupException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)