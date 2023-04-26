from bs4 import BeautifulSoup
from datetime import date
from datetime import timedelta
import re
import requests

# Dictionary to sub team names for team abbreviations
team_dict = {
    "D'backs": "ARI",
    "Arizona Diamondbacks": "ARI",
    "Braves": "ATL",
    "Atlanta Braves": "ATL",
    "Baltimore Orioles": "BAL",
    "Orioles": "BAL",
    "Red Sox": "BOS",
    "Boston Red Sox": "BOS",
    "Chicago Cubs": "CHC",
    "Cubs": "CHC", 
    "Chicago White Sox": "CHW",
    "White Sox": "CHW",
    "Cincinnati Reds": "CIN",
    "Reds": "CIN",
    "Cleveland Guardians": "CLE",
    "Guardians": "CLE",
    "Colorado Rockies": "COL",
    "Rockies": "COL",
    "Detroit Tigers": "DET",
    "Tigers": "DET",
    "Miami Marlins": "MIA",
    "Marlins": "MIA",
    "Houston Astros": "HOU",
    "Astros": "HOU",
    "Kansas City Royals": "KC",
    "Royals": "KC",
    "Los Angeles Angels": "LAA",
    "Angels": "LAA",
    "Los Angeles Dodgers": "LAD",
    "Dodgers": "LAD",
    "Milwaukee Brewers": "MIL",
    "Brewers": "MIL",
    "Minnesota Twins": "MIN",
    "Twins": "MIN",
    "New York Mets": "NYM",
    "Mets": "NYM",
    "New York Yankees": "NYY",
    "Yankees": "NYY",
    "Oakland Athletics": "OAK",
    "Athletics": "OAK",
    "Philadelpha Phillies": "PHI",
    "Phillies": "PHI",
    "Pittsburgh Pirates": "PIT",
    "Pirates": "PIT",
    "San Diego Padres": "SD",
    "Padres": "SD",
    "San Francisco Giants": "SF",
    "Giants": "SF",
    "Seattle Mariners": "SEA",
    "Mariners": "SEA",
    "St. Louis Cardinals": "STL",
    "Cardinals": "STL",
    "Tampa Bay Rays": "TB",
    "Rays": "TB",
    "Texas Rangers": "TX",
    "Rangers": "TX",
    "Toronto Blue Jays": "TOR",
    "Blue Jays": "TOR",
    "Washington Nationals": "WAS",
    "Nationals": "WAS"
}

# Grab current date and day before 
today = date.today()
d = timedelta(days = 1)
todaymin1 = today - d
d1 = todaymin1.strftime("%d/%m/%Y")
today = today.strftime("%d/%m/%Y")

# Scrape for previous day's winners
def scrape_for_scores(date):
    day, month, year = date.rstrip().split('/')
    query = '?year=' + year + '&month=' + month + '&day=' + day

    r = requests.get(f"https://www.baseball-reference.com/boxes/{query}")
    soup = BeautifulSoup(r.content, 'html5lib')

    scoreboard = soup.findAll('tr', attrs= {"class": "winner"})
    winners = []

    for game in scoreboard:
        out_str = game.text
        out_str = out_str.rstrip()
        out_str = re.sub('[0-9]', '', out_str)
        out_str = out_str.replace('Final', '')
        out_str = out_str.replace('()', '')
        out_str = out_str.replace('\n', '')
        out_str = out_str.replace('\t', '')
        out_str = team_dict[out_str]
        if out_str != '':
            winners.append(out_str)
    
    return winners

# Scrape for today's matchups 
def scrape_for_next_games():

    r = requests.get("https://www.baseball-reference.com/previews/")
    soup = BeautifulSoup(r.content, 'html5lib')

    matchups = soup.findAll('table', attrs={'class': 'teams'})
    match_out = []

    for matchup in matchups:
        teams = matchup.findAll('a')
        team_list = []
        for team in teams:
            if team.text == 'Preview':
                continue
            else:
                out_str = team.text
                out_str = out_str.rstrip().strip()
                out_str = re.sub('[0-9]', '', out_str)
                out_str = out_str.replace('Preview', '')
                out_str = out_str.replace('(-)', '')
                out_str = out_str.replace(':PM', '')
                out_str = team_dict[out_str]
                team_list.append(out_str)

        match_out.append(team_list)                   

    return match_out

teams_won = scrape_for_scores(d1)
tmr_matchups = scrape_for_next_games()

# Send update request to API to update previous games 
url = 'http://localhost:8000/v1/api/update/?type=winners'
obj = {"winners": teams_won,
       "date": d1}
requests.post(url, json = obj)

# Send update request to API to add today's games 
url = 'http://localhost:8000/v1/api/update/?type=matchups'
obj = {"matchups": tmr_matchups, 
       "date": today}
requests.post(url, json = obj)


