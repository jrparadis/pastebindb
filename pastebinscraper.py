import urllib.request
from bs4 import BeautifulSoup
import random
import time
import sqlite3

dbc = sqlite3.connect('pastebin.db')
cur = dbc.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS paste(url TEXT, text TEXT)')

while(1):
    response = urllib.request.urlopen('https://pastebin.com/')
    ilikesoup = BeautifulSoup(response, 'lxml')
    thing = ilikesoup.find_all(['a'])
    youareel = []
    for each in thing[10:18]:
        youareel.append('https://www.pastebin.com' + each.get('href'))

    for stuff in youareel:
        randompaste = urllib.request.urlopen(stuff)
        thetext = BeautifulSoup(randompaste, 'html.parser')
        newerthing = thetext.find_all('ol', class_="text")
        thedata = ''
        for athing in newerthing:
            thedata += athing.get_text()
        print (thedata)
        cur.execute('INSERT INTO paste VALUES(?, ?)', [str(stuff),str(thedata)])
        dbc.commit()
        time.sleep(5)
    time.sleep(5)
