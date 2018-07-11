import requests
import bs4
import re
import pandas as pd
from colorama import Fore, Style
import json

query=input("Enter the name of the team exactly as in HLTV: ")
checkQuery=query

url='https://www.hltv.org/search?query='+query
page=requests.get(url)

soup = bs4.BeautifulSoup(page.text, 'lxml')

name=soup.find('a', text=query)
print (Fore.RED + "################")
print(name.contents[0])
print ("################\n" + Style.RESET_ALL)

if(len(checkQuery.split())==1):
    nameLower=query.lower()
else:
    nameLower=checkQuery.split()[0].lower()+'-'+checkQuery.split()[1].lower()

for link in soup.find_all('a'):
    links=link.get('href')

    matchObj = re.search(r'/team/[0-9]{4}/'+nameLower, links)
    if matchObj:
        team_url=matchObj.group()
        break

team_link='https://www.hltv.org/' + team_url
page2=requests.get(team_link)

soup2 = bs4.BeautifulSoup(page2.text, 'lxml')

team = soup2.select(".bodyshot-team a")
for player in team:
    print (player.get('title'))


rankWeeks = soup2.select('.profile-team-stat > span')

print ("\n")
print ("Current World Ranking: " + rankWeeks[0].text)
print ("Weeks on top30 for core: " + rankWeeks[1].text + "\n")

print (Fore.BLUE + "################")
print ("Recent Results")
print ("################\n" + Style.RESET_ALL)

results = soup2.select('.results-holder table tr div.team')


matches = []
for teamName in results[1::2]:
    item = query + " vs "+teamName.getText()
    matches.append(item)

results2 = soup2.select('.results-holder table tr td.result-score span')

scores = []
for score in results2:
    scores.append(score.getText())

scoresAll = []
for i,k in zip(scores[0::2], scores[1::2]):
    item2 = str(i) + "-" + str(k)
    scoresAll.append(item2)


results3 = soup2.select('.results-holder table tr td.event span')

events = []
for event in results3:
    events.append(event.getText())


resultsAll=pd.DataFrame({
    'Score': scoresAll,
    'Matchup': matches,
    'Tournament': events
})

print (resultsAll)
print ("\n")

print (Fore.GREEN + "################")
print ("Ongoing and Upcoming Events")
print ("################\n" + Style.RESET_ALL)

upcoming = soup2.select('div.upcoming-events-holder a.ongoing-event div.text-ellipsis')

upcomingEvents = []
for event in upcoming:
    item = event.getText() 
    upcomingEvents.append(item)


upcomingDate = soup2.select('div.upcoming-events-holder a.ongoing-event tr.eventDetails span span span')

upcomingDates=[]

for date in upcomingDate:
    upcomingDates.append(date.getText())

eventDates=[]
for i, j in zip(upcomingDates[0::3], upcomingDates[1::3]):
    item = i + j
    eventDates.append(item)

upcomingSeries=pd.DataFrame({
    'Event': upcomingEvents,
    'Date': eventDates
})

print (upcomingSeries)
print ("\n")

print (Fore.MAGENTA + "################")
print ("Big Team Achievements")
print ("################\n" + Style.RESET_ALL)

achievements=soup2.select('.two-col .col')
for achieve in achievements:
    print (achieve.getText())


print (Fore.YELLOW + "################")
print ("Map Win Percentage")
print ("################\n" + Style.RESET_ALL)

graph = soup2.select('.standard-box > div.graph')
d=json.loads(graph[1].get('data-fusionchart-config'))
maps = d['dataSource']['categories'][0]['category']
mapsPlayed=[]
for m in maps:
    mapsPlayed.append(m['label'])

win = d['dataSource']['dataset'][0]['data']
winPer=[]
for val in win:
    winPer.append(val['value'])

ct = d['dataSource']['dataset'][1]['data']
ctWinPer=[]
for val in ct:
    ctWinPer.append(val['value'])

t=d['dataSource']['dataset'][2]['data']
tWinPer=[]
for val in t:
    tWinPer.append(val['value'])

tp=d['dataSource']['dataset'][3]['data']
tPlayed=[]
for val in tp:
    tPlayed.append(val['value'])

mapWinPercentage = pd.DataFrame({
    'Map': mapsPlayed,
    'Win%': winPer,
    'CT Win%': ctWinPer,
    'T Win%': tWinPer,
    'Times Played': tPlayed
})

print (mapWinPercentage)








