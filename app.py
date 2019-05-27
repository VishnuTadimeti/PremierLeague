from flask import Flask, render_template
import requests, json

app = Flask(__name__)

# Football-Data.org
headers = { 'X-Auth-Token': 'TOKEN_HERE'}

req_table = requests.get("http://api.football-data.org/v1/competitions/445/leagueTable", headers = headers)
req_fixtures = requests.get("http://api.football-data.org/v1/competitions/445/fixtures", headers = headers)
req_gameweek = requests.get("http://api.football-data.org/v1/competitions/445", headers = headers)
req_team = requests.get("http://api.football-data.org/v1/competitions/445/teams", headers = headers)

res_table = json.loads(req_table.text)
res_fixtures = json.loads(req_fixtures.text)
res_gameweek = json.loads(req_gameweek.text)
res_team = json.loads(req_team.text)

pl_table = res_table['standing']
pl_fixtures = res_fixtures['fixtures']
pl_current_gameweek = res_gameweek['currentMatchday']
pl_team = res_team['teams']

####################################################################

# This is for the Predictions page
home_team_name = []
away_team_name = []
home_team_crest = []
away_team_crest = []

# This is for the Teams page
teams_name = []
teams_crest = []

# This is for the PL Table
standings_position = []
standings_crest = []
standings_name = []
standings_mp = []
standings_win = []
standings_draw = []
standings_loss = []
standings_gf = []
standings_ga = []
standings_gd = []
standings_points = []

# Fixtures for current gameweek with crests
for i in range(0, 380):
    status = pl_fixtures[i]['status']
    if status == 'SCHEDULED' or 'TIMED':
        if pl_fixtures[i]['matchday'] == pl_current_gameweek:
            home_team_name.append(pl_fixtures[i]['homeTeamName'])
            away_team_name.append(pl_fixtures[i]['awayTeamName'])
            for k in range(0, 20):
                if pl_fixtures[i]['homeTeamName'] == pl_team[k]['name']:
                    home_team_crest.append(pl_team[k]['crestUrl'])

                if pl_fixtures[i]['awayTeamName'] == pl_team[k]['name']:
                    away_team_crest.append(pl_team[k]['crestUrl'])

# PL Table
for i in range(0, 20):
    standings_position.append(pl_table[i]['position'])
    standings_crest.append(pl_table[i]['crestURI'])
    standings_name.append(pl_table[i]['teamName'])
    standings_mp.append(pl_table[i]['playedGames'])
    standings_win.append(pl_table[i]['wins'])
    standings_draw.append(pl_table[i]['draws'])
    standings_loss.append(pl_table[i]['losses'])
    standings_gf.append(pl_table[i]['goals'])
    standings_ga.append(pl_table[i]['goalsAgainst'])
    standings_gd.append(pl_table[i]['goalDifference'])
    standings_points.append(pl_table[i]['points'])

# Teams Page
for i in range(0, 20):
    teams_name.append(pl_team[i]['name'])
    teams_crest.append(pl_team[i]['crestUrl'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/fixtures')
def fixtures():
    return render_template('fixtures.html', fixtures = zip(home_team_name, away_team_name, home_team_crest, away_team_crest))

@app.route('/teams')
def teams():
    return render_template('teams.html', fixtures = zip(teams_name, teams_crest))

@app.route('/predictions/<home_predict>-<away_predict>')
def predictions(home_predict, away_predict):
    # Get CrestURI for the predictions page
    for k in range(0, 20):
        if home_predict == pl_team[k]['name']:
            home_crest_predict = pl_team[k]['crestUrl']

        if away_predict == pl_team[k]['name']:
            away_crest_predict = pl_team[k]['crestUrl']
    return render_template('predictions.html', home_team = home_predict, away_team = away_predict, home_team_crest = home_crest_predict, away_team_crest = away_crest_predict)

@app.route('/standings')
def standings():
    return render_template('standings.html', team = zip(standings_position,
                                                        standings_crest,
                                                        standings_name,
                                                        standings_mp,
                                                        standings_win,
                                                        standings_draw,
                                                        standings_loss,
                                                        standings_gf,
                                                        standings_ga,
                                                        standings_gd,
                                                        standings_points))

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)