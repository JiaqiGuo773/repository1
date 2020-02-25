import requests
import json
import pymysql
from ipykernel.tests import tmp

url="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=7a0ee16c2311e8aaf0dd46322e64a4ed3e2a8069"
text_page=requests.get(url).text
with open("dynamic.json", "w") as file:
    file.write(text_page)
    
conn = pymysql.connect(
        host = 'database-1.cwouctjtnr0b.eu-west-1.rds.amazonaws.com',
        port = 3306,
        user = 'admin',
        passwd = 'jo91TKYJs0czd6DAu4M1',
        db = 'dbikes',)
       
cur = conn.cursor() 

'''sql = """CREATE TABLE station (
    number INTEGER, 
    contract_name VARCHAR(256), 
    name VARCHAR(256), 
    address VARCHAR(256), 
    position_lat REAL, 
    position_lng REAL, 
    banking VARCHAR(100), 
    bonus VARCHAR(100), 
    bike_stands INTEGER, 
    available_bike_stands INTEGER, 
    available_bikes INTEGER,
    status VARCHAR(100), 
    last_update VARCHAR(100))"""

cur.execute(sql)'''

a=open(r"dynamic.json", "r")

out = a.read()
tmp = json.loads(out)
num = len(tmp)
i=0
while i < num:
    numbe = tmp[i]['number']
    contract_name  = tmp[i]['contract_name']
    name = tmp[i]['name']
    address = tmp[i]['address'] 
    position_lat = tmp[i]['position']['lat']
    position_lng = tmp[i]['position']['lng']
    banking = tmp[i]['banking']
    bonus = tmp[i]['bonus']
    bike_stands = tmp[i]['bike_stands']
    available_bike_stands = tmp[i]['available_bike_stands']
    available_bikes = tmp[i]['available_bikes']
    status = tmp[i]['status'] 
    last_update = tmp[i]['last_update']
    value = [numbe, contract_name, name, address, position_lat, position_lng, banking, bonus, bike_stands, available_bike_stands, available_bikes, status, last_update]
    sql_insert =("insert into station(numbe, contract_name, name, address, position_lat, position_lng, banking, bonus, bike_stands, available_bike_standsble, available_bikes, status, last_update) values (%d,%s,%s,%s,%f,%f,%s, %s, %d, %d, %d, %s, %s);",value)
    print(sql_insert)
    
    cur.execute(sql_insert)
    i+=1
conn.commit()
