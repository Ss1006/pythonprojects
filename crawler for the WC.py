
import requests
import json
import mechanize
from bs4 import BeautifulSoup
import time
import cPickle as pickle

br = mechanize.Browser()
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=10)
br.addheaders = [('user-agent','Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36  (KHTM, like Gecko/44.0.2403.157 Safari/537.36)')]

starting_link = 'http://data.huffingtonpost.com/2014/world-cup'
response = mechanize.urlopen(starting_link)
soup = BeautifulSoup(response)

links_html = soup.find_all("span",class_ = "matchup")
links = []
for link_html in links_html:
    a = link_html.find_all('a')
    for l in a:
        link = l.get('href')
        link = link.split('/')[-1]

    links.append(link)

def get_match_data(match):
    match_id = match.split('/')[-1]
    response = mechanize.urlopen('http://data.huffingtonpost.com/2014/world-cup/matches/%s.json' % match_id)
    match_data = json.loads(response.read())
    return match_data
# match_data = get_match_data(links[0])
# match_data.keys()


def get_match_names(match):
    response = mechanize.urlopen('http://data.huffingtonpost.com/2014/world-cup/matches/%s' % links[0])
    soup = BeautifulSoup(response)

    data = {}

    data_script = soup.find_all("script")[1]
    data_lines = data_script.text.split('\n')

    for line in data_lines:
        try:
            line_data = line.split('=')
            name = line_data[0].split('.')[1]
            value = json.loads(line_data[1][-1])
            data[name] = value
        except:
            print "Pass the line......",line
    return data
# names = get_match_names(links[0])
# names.keys

data = {}
for match in links:
    if match not in data:
        print match
        time.sleep(10)

        match_data = get_match_data(match)
        match_names = get_match_names(match)
        data[match] = {'data':match_data,'names':match_names}

        print match, "done"
    else:
        print match, "already processed"
print len(data.keys())

data['germany-vs-algeria-731820']

pickle.dump(data,open('wc2014.p','wb'))
data == pickle.load(open('wc2014.p','rb'))



