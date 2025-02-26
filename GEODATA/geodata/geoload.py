from urllib import parse, request
import sqlite3
import json
import time
import ssl


# Google API (requires API key)
# api_key ='AIzaSyAwf6DNCxyJN-0NsaF5iiiCxhvtET7Iupg'
# serviceurl = "http://maps.googleapis.com/maps/api/geocode/json?"

# If you are in China this URL might work (with key):
# serviceurl = "http://maps.google.cn/maps/api/geocode/json?"

serviceurl = "http://python-data.dr-chuck.net/geojson?"


# Deal with SSL certificate anomalies Python > 2.7
# scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
scontext = None

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

fh = open("where.data")
count = 0
for line in fh:
    if count > 200 : 
        print('Retrieved 200 locations, restart to retrieve more')
        break
    address = line.strip()
    print('')
    cur.execute("SELECT geodata FROM Locations WHERE address= ?", ((address), ))

    try:
        data = cur.fetchone()[0]
        print ("Found in database ", address)
        continue
    except:
        pass

    print('Resolving', address)
    url = serviceurl + parse.urlencode({"sensor":"false", "address": address})
    print('Retrieving', url)
    uh = request.urlopen(url, context=scontext)
    data = uh.read().decode()
    print('Retrieved', len(data), 'characters', data[:20].replace('\n', ' '))
    count = count + 1
    try: 
        js = json.loads(str(data))
        # print js  # We print in case unicode causes an error
    except: 
        continue

    if 'status' not in js or (js['status'] != 'OK' and js['status'] != 'ZERO_RESULTS') : 
        print('==== Failure To Retrieve ====')
        print(data)
        continue

    cur.execute('''INSERT INTO Locations (address, geodata) 
            VALUES ( ?, ? )''', ((address, data)))
    conn.commit() 
    if count % 10 == 0 :
        print('Pausing for a bit...')
        time.sleep(5)

print ("Run geodump.py to read the data from the database so you can visualize it on a map.")
