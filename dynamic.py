import requests
import pymysql
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback 
import glob 
import os
from pprint import pprint
import simplejson as json
import time
from IPython.display import display


url="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=7a0ee16c2311e8aaf0dd46322e64a4ed3e2a8069"
text_page=requests.get(url).text
with open("dynamic.json", "w") as file:
    file.write(text_page)
    

URI = 'database-1.cwouctjtnr0b.eu-west-1.rds.amazonaws.com'
PORT = '3306'
DB = 'dbikes'
PASSWORD = 'jo91TKYJs0czd6DAu4M1'
USER="admin"


engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

sql="CREATE DATABASE IF NOT EXISTS dbikes;"

engine.execute(sql)

#sql = "CREATE TABLE dynamic (number INT, contract_name VARCHAR(100), name VARCHAR(100),address VARCHAR(100),position_lat VARCHAR(100), position_lng VARCHAR(100),banking VARCHAR(100), bonus VARCHAR(100), bike_stands INT, available_bike_stands INT, available_bikes INT,status VARCHAR(100), last_update  VARCHAR(100));"

