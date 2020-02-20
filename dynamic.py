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
        db = 'mysql',
        charset = 'utf8',
    )
cur = conn.cursor() 

sql = "CREATE TABLE dynamic (number INT, contract_name VARCHAR(100), name VARCHAR(100),address VARCHAR(100),position_lat VARCHAR(100), position_lng VARCHAR(100),banking VARCHAR(100), bonus VARCHAR(100), bike_stands INT, available_bike_stands INT, available_bikes INT,status VARCHAR(100), last_update  VARCHAR(100));"

cur.execute(sql)