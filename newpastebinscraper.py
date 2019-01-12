#scrapes pastebin and logs it to a sqlite database, basically turns the console into a crappy chatroom that is mostly spam, code, weird chat logs, and misc leaks & dumps - interesting for those interested in security / open data / etc.
#lifetime API access was only $20 so I bought it after being banned 3 or 4 times, heh. 
#requires you to whitelist your IP at https://pastebin.com/doc_scraping_api instead of using creds

import requests
import sqlite3
import time


pastebin = sqlite3.connect('newpastebin.db')
cur = pastebin.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS paste(key TEXT, user TEXT, title TEXT, expire INT, date INT, size INT, syntax TEXT, pastecontent TEXT)')

while(1):
    pastes = requests.get('https://scrape.pastebin.com/api_scraping.php?limit=250')
    keydb = cur.execute("SELECT key FROM paste").fetchall()
    for each in pastes.json():
        if each['key'] in str(keydb):
            pass
        else:
            key = each['key']
            user = each['user']
            if user == '':
                user = ''
            title = each['title']
            if title == '':
                title = ''
            expire = each['expire']
            date = each['date']
            size = each['size']
            syntax = each['syntax']
            pastecontent = ''
            newcontent = requests.get(f'https://scrape.pastebin.com/api_scrape_item.php?i={key}')
            #edit int(size) comparison to print larger pastes to console - default 800 isn't too large.
            if expire is not '0' or int(size) <= 800:
                try:
                    print(newcontent.text)
                except Exception as e:
                    print(e)
            cur.execute('INSERT INTO paste VALUES(?,?,?,?,?,?,?,?)',[key,user,title,expire,date,size,syntax,newcontent.text])
            try:
                print(f'https://scrape.pastebin.com/{key}',date,f'{expire:<8}',f'{size:<16}',f'{syntax:<6}',f'{user:<20}',title)
            except:
                print(f'error: https://scrape.pastebin.com/{key}')
            time.sleep(3)
    timesleep = 15
    time.sleep(timesleep)
    pastebin.commit()
    
