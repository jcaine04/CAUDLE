from flask import render_template, redirect

from app import app

from main import Team, Conference

@app.route('/')
@app.route('/index')
def index():
    return 'Hello world!'

@app.route('/getteams')
def getteams():
    team = Team()
    team_urls = team.get_roster_urls()
    return render_template('teams.html', team_urls=team_urls)

@app.route('/addconferencesandteams')
def add_conferences_and_teams():
    team = Team()
    team.add_all_conferences_and_teams()
    return "Successfully added all conferences and teams."

@app.route('/addallrosters')
def add_all_rosters():
    team = Team()
    team.add_all_rosters()
    return "Successfully added all rosters."