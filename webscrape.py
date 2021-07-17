import requests
from bs4 import BeautifulSoup

URL = "https://www.hltv.org/matches"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

live_matches_DIVS = soup.find_all("div", {"class": "liveMatch"})
upcoming_matches_DIVS = soup.find_all("div", {"class": "upcomingMatch"})

def find_stared_matches(soup_data):
    stared_matches = {}
    for match in soup_data:
        if match.find("i", {"class": "fa fa-star"}):
            if (match.find_all("div", {"class": "matchTeams"})):
                teams = match.find_all("div", {"class": "matchTeamName"})
                if len(teams) < 2:
                    break
                stared_matches['team1'] = teams[0].text.lstrip().rstrip()
                stared_matches['team2'] = teams[1].text.lstrip().rstrip()
            if (match.find("a", {"class": "match a-reset"})['href']):
                stared_matches["url"] = match.find("a", {"class": "match a-reset"})['href']

            if (match.find_all("div", {"class": "matchEventName"})):
                stared_matches['tournament'] = match.find("div", {"class": "matchEventName"}).text.lstrip().rstrip()
    return stared_matches

def find_all_stared_matches():
    live_stared_matches = find_stared_matches(live_matches_DIVS)
    upcoming_stared_matches = find_stared_matches(upcoming_matches_DIVS)
    all_stared_matches = live_stared_matches | upcoming_stared_matches
    return(all_stared_matches)
