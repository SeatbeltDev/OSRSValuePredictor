'''
CHANDLER MATEKA
Final Project - Program #1: Data Collection

Resources:
    Textbook
    https://docs.python.org/3/library/re.html
        I used re.sub to remove the suffix of titles based on a regex

Item pages: https://oldschool.runescape.wiki/w/Head_slot_table
Attributes scraped for main part (head items):
    title - title
    released - release date of item
    members - does it require paid membership to obtain
    quest items - is it used specifically for a quest
    items - can it be traded between players
    worn equipment - can a player wear it
    stackable items - can it be stacked in one slot in a player's inventory
    note - can it be exchanged for a bank note
    destroy - is it destroyed or dropped on the floor when dropped
    examine - item description
    value - store value
    high level alchemy - value when the high alchemy spell is used on it
    low level alchemy - value when the low alchemy spell is used on it
    weight - weight
    RuneScape:Grand Exchange Market Watch - value in player market
    grand exchange - buy limit on player market per 4 hours
    twisted league - is it available on twisted league (a separate gamemode)
Attributes for weapon table scraped:
    Members: does it require members to obtain
    All available item stats: (self explanatory)
        Stab attack, Slash attack, Crush attack
        Magic attack, Ranged attack,
        Stab defence, Slash defence, Crush defence
        Magic defence, Ranged defence
        Strength, Ranged Strength, Magic Damage
        Prayer, Speed

Link to page with table: https://oldschool.runescape.wiki/w/Head_slot_table
'''
import requests
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup
import re
import json


#global vars
home = 'https://oldschool.runescape.wiki'
start = 'https://oldschool.runescape.wiki/w/Worn_Equipment'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.487'}
rp = RobotFileParser()
siteDicts = []

#get rp based on a robots.txt
def get_rp(robots):
    print(robots)

    #download and parse page
    r = requests.get(robots, headers = headers)

    #parse
    rp.parse(r.text.split('\n'))

    return rp

def get_page(url):
    print(url)

    if rp.can_fetch('*', url) == True:
        r = requests.get(url, headers = headers)
        bs = BeautifulSoup(r.text, 'html.parser')
        return bs
    else:
        print('URL cannot be fetched')
        return None

#Main

robots = 'https://oldschool.runescape.wiki/robots.txt'
get_rp(robots) #Do I need the returned rp?
bs = get_page(start)
print()

#all equipment slot tables
equipLists = bs.find_all('a', title = re.compile('slot table$'))


'''
Scrape item slot tables
'''


# scrape data for all items from all 12 tables of equipment items
for equipList in equipLists:
# for i in range(1):
    # equipList = equipLists[2]

    # get page and the item table on it
    ext = equipList.attrs['href']
    url = f'{home}{ext}'
    if 'Special' in url: continue

    page = get_page(url)
    table = page.find('table', class_ = 'wikitable')
    itemType = page.title.get_text().replace(' slot table - OSRS Wiki', '')
    print()
    
    # get list of col/attribute names for item stats
    colNames = [] 
    for col in table.tbody.select('tr')[0]:
        if col.img == None: continue # skip filler/padding columns
        colNames.append(col.img['title'])
    colNames = colNames[1:] # remove first col, not needed


    # for each equipment slot table, get the first 5 items and scrape some attributes
    for item in table.tbody.find_all('tr')[1:len(table.tbody)]: # skip heading row, capped at 5 items for now
        pageDict = {}

        # item data from table
        for col in range(3,len(item.select('td'))):
            c = item.select('td')[col]
            
            attrib = colNames[col-3]
            val = c.get_text()
            
            print(f'{attrib}: {val}')
            pageDict[attrib] = val

        # click item page
        ext = item.find('a').attrs['href']
        url = f'{home}{ext}'
        if 'Special' in url: continue
        page = get_page(url)

        pageDict['Type'] = itemType
        print(f'Type: {itemType}')
        
        title = page.title.get_text()
        title = title.replace(' - OSRS Wiki', '')
        pageDict['Title'] = title
        print(title)


        # item data from item page
        table = page.find('table')
        geFix = 0

        # weirdTable = table.tbody.select('tr')[0].select_one('a').attrs.get('title')
        # if 'Money making' in weirdTable or 'Update:Optional' in weirdTable:
        #     table = page.find_all('table')[1]
        # print(f'AAAAAAA: {len(table.tbody.select("tr"))}')
        if len(table.tbody.select("tr")) < 3:
            table = page.find_all('table')[1]

        for row in table.tbody.select('tr'):
            if row.select('a') == []: continue # skip padding/filler rows

            attrib = row.select_one('a').attrs.get('title')
            val = row.select_one('td').get_text()
            
            if attrib == None or val == None: continue # another filler check

            # clean up 
            # fix released attribute name being wrong
            if re.match('^\d{1,31}', attrib):
                attrib = 'Released'
                val = val.replace(' (Update)', '')
            elif 'coin' in val:
                val = val.split()[0].replace(',', '')
            
            if 'Grand Exchange' in attrib:
                if geFix == 0:
                    attrib = 'GE Value'
                    geFix += 1
                elif geFix == 1:
                    attrib = 'GE Buy Limit'
                    geFix += 1
                else:
                    attrib = 'GE Daily Volume'

            # elif 'Grand Exchange' in attrib:
            #     attrib = 'GE Buy Limit'

            print(f'{attrib}: {val}')
            pageDict[attrib] = val

        print()
        # append page dictionary to list of dicts
        siteDicts.append(pageDict)


with open('equipmentData.json', 'w') as fp:
    json.dump(siteDicts, fp)

print('\nTotal number of equipment items scraped:', len(siteDicts))
