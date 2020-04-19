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
    weather_main = tmp['weather_main']
    weather_description = tmp['weather_description']
    temp = tmp['temp']
    feels_like = tmp['feels_like']
    temp_min = tmp['temp_min']
    temp_max = tmp['temp_max'] 
    pressure = tmp['pressure']
    humidity = tmp['humidity']
    visibility = tmp['visibility']
    wind_speed = tmp['wind_speed']
    wind_deg = tmp['wind_deg']
    clouds_all = tmp['clouds_all']
    rain_1h = tmp['rain_1h']
    rain_3h = tmp['rain_3h']
    snow_1h = tmp['snow_1h']
    snow_3h = tmp['snow_3h']
    dt = tmp['dt']
    sunrise = tmp['sunrise']
    sunset = tmp['sunset']
    
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