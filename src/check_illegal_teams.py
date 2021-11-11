import requests
from bs4 import BeautifulSoup

league_id = 26

ottoneu_lg_url = f'https://ottoneu.fangraphs.com/basketball/{league_id}/'
r = requests.get(ottoneu_lg_url)
soup = BeautifulSoup(r.content, 'html.parser')
standings_table = soup.find('div', {'class':'split-layout'}).find('section', {'class':'section-container'}).find('table')
over_limit_teams = list()
for row in standings_table.find_all("tr"):
    if row.get("class") is not None and row.get("class").pop() == 'team-over-limit':
        team_name = row.get_text().split("\n")[1] # assumes newlines not allowed in team names
        team_id = row.a['href'].split("/")[-1]
        over_limit_teams.append((team_id, team_name))

# how to do the days?
