import requests
from bs4 import BeautifulSoup

URL = "https://www.hltv.org/matches?predefinedFilter=top_tier"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

live_matches_DIVS = soup.find_all("div", {"class": "liveMatch"})
upcoming_matches_sections = soup.find_all("div", {"class": "upcomingMatchesSection"})

def find_stared_matches(soup_data):
    matches_list = {}
    counter = 0
    for match_section in soup_data:
        upcoming_matches_DIVS = match_section.find_all("div", {"class": "upcomingMatch"})
        match_day_headline_DIV = match_section.find("span", {"class": "matchDayHeadline"})
        date = match_day_headline_DIV.text
        
        for match in upcoming_matches_DIVS:
            matches_list[counter] = {}

            is_a_empty_match = match.find_all("div", {"class": "matchInfoEmpty"})
            if is_a_empty_match:
                continue

            teams = match.find_all("div", {"class": "matchTeamName"})
            if len(teams) < 2: continue

            matches_list[counter]['team1'] = teams[0].text.lstrip().rstrip()
            matches_list[counter]['team2'] = teams[1].text.lstrip().rstrip()
            matches_list[counter]["url"] = match.find("a", {"class": "match a-reset"})['href']

            if (match.find_all("div", {"class": "matchEventName"})):
                matches_list[counter]['tournament'] = match.find("div", {"class": "matchEventName"}).text.lstrip().rstrip()

            time_of_day = match.find("div", {"class": "matchTime"}).text
            matches_list[counter]['date'] = date + "-" + time_of_day.replace(":", "-")

            counter += 1
    return matches_list

#        is_a_star_match = match.find("i", {"class": "fa fa-star"})
#        if is_a_star_match:


def find_all_stared_matches():
    live_stared_matches = find_stared_matches(live_matches_DIVS)
    upcoming_stared_matches = find_stared_matches(upcoming_matches_sections)
    print(len(live_stared_matches))
    print(len(upcoming_stared_matches))
    all_stared_matches = live_stared_matches | upcoming_stared_matches #Doesnt work. Only gives upcoming_stared_matches
    print(len(all_stared_matches))
    return(all_stared_matches)
