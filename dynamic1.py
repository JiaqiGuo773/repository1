import requests
import json
import pymysql

url="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=7a0ee16c2311e8aaf0dd46322e64a4ed3e2a8069"
text_page=requests.get(url).text
with open("dynamic.json", "w") as file:
    file.write(text_page)
    
conn = pymysql.connect(
        host = 'database-1.cwouctjtnr0b.eu-west-1.rds.amazonaws.com',
        port = 3306,
        user = 'admin',
        passwd = 'jo91TKYJs0czd6DAu4M1',
        db = 'dbikes',
       
cur = conn.cursor() 

sql = "CREATE TABLE station (number INTEGER, contract_name VARCHAR(256), name VARCHAR(256), address VARCHAR(256), position_lat REAL, position_lng REAL, banking VARCHAR(100), bonus VARCHAR(100), bike_stands INTEGER, available_bike_stands INTEGER, available_bikes INTEGER,status VARCHAR(100), last_update VARCHAR(100))"

cur.execute(sql)