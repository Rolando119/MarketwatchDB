# -*- coding: utf-8 -*-

!pip install mysql-connector

import requests
import datetime

url = 'https://prices.runescape.wiki/api/v1/osrs'
header = {
    'User-Agent': 'price_tracker',
    'DiscordU': 'jinx_shrimp'
}
response = requests.get(url + '/latest', headers = header)
responseN = requests.get(url + '/mapping', headers = header)
response.close()
responseN.close()

name_data = responseN.json()
NAMES_IDS = {}
for i in name_data:
  NAMES_IDS[i['name']] = i['id']

responseN.close()
response = requests.get(url + '/latest', headers = header)
response.close()
price_data = response.json()

import mysql.connector

db = mysql.connector.connect(
    host = 'DummyHost.com',
    user = 'sql234124',
    password = 'Password',
    database = 'sql234124'
)


dbc = db.cursor()

#inputs a string with the item name.
#inserts an item with it's ID and name into the Items table of the database.
def insert_item(name):
  name = name.capitalize()
  if name not in NAMES_IDS:
    print('Item not found\n-------------------------------')
    return
  dbc.execute('SELECT ItemID FROM Items')
  ids = dbc.fetchall()
  itemID = NAMES_IDS[name]
  for id in ids:
    bl = itemID in id
    if bl:
      break
  if bl:
    print('Item already exists in the database\n-------------------------------')
    return
  else:
    dbc.execute('INSERT INTO Items (ItemID, Name) VALUES (%s, %s)', (itemID, name))
    db.commit()
    print('Item has been entered into the database\n--------------------------------------')

#inputs a string with the item name, and a count for the unique transaction number.
#inserts the price of that item, along with it's unique ID on the date it was sold, along with the time
#it was sold at into the database table Price.
def insert_price(name, i):
  name = name.capitalize()
  if name not in NAMES_IDS:
    print('Item not found\n-------------------------------')
    return
  itemID = NAMES_IDS[name]
  item_price = price_data['data'][str(itemID)]
  lower = item_price['low']
  upper = item_price['high']
  date = datetime.date.today()
  time = datetime.datetime.now().time()
  avgprice = (item_price['high'] + item_price['low']) / 2
  dbc.execute('INSERT INTO Price (TransNum, ItemID, Cost, DoT, ToT, LowerBound, UpperBound) VALUES (%s, %s, %s, %s, %s, %s, %s)', (i, itemID, avgprice, date, time, lower, upper))
  db.commit()
  print('Item transaction has been entered into the database\n--------------------------------------')

insert_price('voidwaker', 1)
