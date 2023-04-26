from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date
from datetime import timedelta
import re
import requests


game_dict = {}

today = date.today()
d = timedelta(days = 1)
todaymin1 = today - d
d1 = todaymin1.strftime("%d/%m/%Y")
today = today.strftime("%d/%m/%Y")

def scrape_for_scores(date):
    day, month, year = date.rstrip().split('/')
    query = '?year=' + year + '&month=' + month + '&day=' + day
    
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as wd:

        wd.get(f"https://www.baseball-reference.com/boxes/{query}")

        scoreboard = wd.find_elements(By.CLASS_NAME, "winner")

        winners = []

        for game in scoreboard:
            out_str = game.text
            out_str = out_str.rstrip()
            out_str = re.sub('[0-9]', '', out_str)
            out_str = out_str.replace('Final', '')
            out_str = out_str.replace('()', '')
            if out_str != '':
                winners.append(out_str)
    
    return winners

def scrape_for_next_games():
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as wd:

        wd.get("https://www.baseball-reference.com/previews/")

        matchups = wd.find_elements(By.CLASS_NAME, "teams")

        match_out = []

        for matchup in matchups:
            out_str = matchup.text
            out_str = out_str.rstrip().strip()
            out_str = re.sub('[0-9]', '', out_str)
            out_str = out_str.replace('Preview', '')
            out_str = out_str.replace('(-)', '')
            out_str = out_str.replace(':PM', '')
            out_str = "".join(out_str.splitlines())

            if out_str == '':
                continue
            else:
                match_out.append(out_str)                   

        return match_out

teams_won = scrape_for_scores(d1)
tmr_matchups = scrape_for_next_games()

url = f'http://localhost:8000/v1/api/update/?type=winners'
obj = {"winners": teams_won}
requests.post(url, json = obj)

url = f'http://localhost:8000/v1/api/update/?type=matchups'
obj = {"matchups": tmr_matchups}
requests.post(url, json = obj)


