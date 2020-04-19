import utils
import requests
import json
import pymysql
import traceback
from datetime import datetime
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
import pandas as pd

f=open(r"weatherload.json", "r")
out = f.read()
f.close()
tmp = json.dumps(out)
tmp = json.loads(out)
num = len(tmp)
conn,cur = utils.get_conn_cur()
i=0
while i < num:
    weather_main = tmp[i]['weather_main']
    weather_description = tmp[i]['weather_description']
    temp = tmp[i]['temp']
    feels_like = tmp[i]['feels_like']
    temp_min = tmp[i]['temp_min']
    temp_max = tmp[i]['temp_max'] 
    pressure = tmp[i]['pressure']
    humidity = tmp[i]['humidity']
    visibility = tmp[i]['visibility']
    wind_speed = tmp[i]['wind_speed']
    wind_deg = tmp[i]['wind_deg']
    clouds_all = tmp[i]['clouds_all']
    rain_1h = tmp[i]['rain_1h']
    rain_3h = tmp[i]['rain_3h']
    snow_1h = tmp[i]['snow_1h']
    snow_3h = tmp[i]['snow_3h']
    dt = tmp[i]['dt']
    sunrise = tmp[i]['sunrise']
    sunset = tmp[i]['sunset']
    
    value = (weather_main, weather_description, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, clouds_all, rain_1h, rain_3h, snow_1h, snow_3h, dt, sunrise, sunset)
    sql_insert ="insert into weather(weather_main, weather_description, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, clouds_all, rain_1h, rain_3h, snow_1h, snow_3h, dt, sunrise, sunset) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"    
    print(sql_insert % value)
    
    try:   
        cur.execute(sql_insert % value)
        conn.commit()
    except Exception as e:
        print(e)
    i+=1
        
cur.close()
conn.close()