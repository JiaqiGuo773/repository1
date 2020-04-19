import requests
import json
import pymysql
import traceback
from datetime import datetime
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
import pandas as pd
import pickle
import utils
import csv

#csvfile = open('a.csv', 'w')
#writer = csv.writer(csvfile,dialect='excel')
#writer.writerow(['weather_main', 'weather_description', 'temp', 'feels_like', 'temp_min', 'temp_max', 'pressure', 'humidity', 'visibility','wind_speed', 'wind_deg', 'clouds_all', 'rain_1h', 'rain_3h', 'snow_1h', 'snow_3h', 'dt', 'sunrise', 'sunset'])
conn,cur = utils.get_conn_cur()
cur.execute("select * from availability;")
data=cur.fetchall
cur.close()
conn.close()
filename='b.csv'
with open(filename,mode='w',encoding='utf-8') as f:
        write = csv.writer(f,dialect='excel')
        for item in data:
            write.writerow(item)


