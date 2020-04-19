import requests
import json
import pymysql
import traceback
from datetime import datetime
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
import pandas as pd
import pickle



def get_db():
    URI ="database-1.cwouctjtnr0b.eu-west-1.rds.amazonaws.com"
    PORT ="3306"
    DB="dbikes"
    USER="admin"
    PASSWORD = "jo91TKYJs0czd6DAu4M1"
    
    return create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER,PASSWORD,URI,PORT,DB),echo=True)



def get_conn_cur():
    conn = pymysql.connect(
        host = 'database-1.cwouctjtnr0b.eu-west-1.rds.amazonaws.com',
        port = 3306,
        user = 'admin',
        password= 'jo91TKYJs0czd6DAu4M1',
        db = 'dbikes',)
               
    cur = conn.cursor()
    return conn,cur

def jcd_file():
    url="https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=7a0ee16c2311e8aaf0dd46322e64a4ed3e2a8069"
    try:
        now=datetime.now()
        
        text_page=requests.get(url).text
        print("jcd file:", now) 
        with open("dynamic.json", "w") as file:
            file.write(text_page)
    except:
        print (traceback.format_exc())    



def weather_file():
    url="http://api.openweathermap.org/data/2.5/weather?q=Dublin,ie&units=metric&appid=62d8e38e8a3f439885a38dcff6e8e86d"
    try:
        now=datetime.now()
        
        text_page=requests.get(url).text
        print("weather file:", now) 
        with open("weather.json", "w") as file:
            file.write(text_page)
    except:
        print (traceback.format_exc())


def create_station():
    conn,cur = get_conn_cur()
    sql = """CREATE TABLE IF NOT EXISTS station (
        number INTEGER, 
        contract_name VARCHAR(256), 
        name VARCHAR(256), 
        address VARCHAR(256), 
        position_lat REAL, 
        position_lng REAL, 
        banking VARCHAR(100), 
        bonus VARCHAR(100), 
        bike_stands INTEGER,
        available_bikes INTEGER, 
        status VARCHAR(100) 
        )"""
    try:
        cur.execute("DROP TABLE IF EXISTS station")
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    cur.close()
    conn.close()

def create_availability():
    conn,cur = get_conn_cur()
    sql = """ CREATE TABLE IF NOT EXISTS availability(
        number INTEGER, 
        available_bikes INTEGER,
        available_bike_stands INTEGER, 
        last_update VARCHAR(100)
        )"""
    try:
        cur.execute(sql)
    except Exception as e:
        print(e)
    cur.close()
    conn.close()
        

def create_weather():
    conn,cur = get_conn_cur()
    sql = """CREATE TABLE IF NOT EXISTS weather (
        weather_main VARCHAR(256), 
        weather_description VARCHAR(256),
        temp VARCHAR(256),
        feels_like VARCHAR(256), 
        temp_min VARCHAR(256), 
        temp_max VARCHAR(256), 
        pressure VARCHAR(256),
        humidity VARCHAR(256),
        visibility VARCHAR(256),
        wind_speed VARCHAR(256),
        wind_deg VARCHAR(256),
        clouds_all VARCHAR(256),
        rain_1h VARCHAR(256),
        rain_3h VARCHAR(256),
        snow_1h VARCHAR(256),
        snow_3h VARCHAR(256),
        dt VARCHAR(256),
        sunrise VARCHAR(256),
        sunset VARCHAR(256)
        )"""
    
    try:
        cur.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
        
    cur.close()
    conn.close()
    
def jcd_to_db():
    f=open(r"dynamic.json", "r")
    out = f.read()
    f.close()
    tmp = json.dumps(out)
    tmp = json.loads(out)
    num = len(tmp)
    conn,cur = get_conn_cur()
    i=0
    while i < num:
        number = tmp[i]['number']
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
        
        value1 = (number, contract_name, name, address, position_lat, position_lng, banking, bonus, bike_stands, available_bikes, status)
        value2 = (number, available_bikes, available_bike_stands, last_update)
        sql_insert1 ='insert into station(number, contract_name, name, address, position_lat, position_lng, banking, bonus, bike_stands, available_bikes, status) values (%d, "%s","%s","%s",%f,%f,"%s", "%s", %d, %d,"%s");' %value1
        sql_insert2 ='insert into availability(number, available_bikes, available_bike_stands, last_update) values (%d, %d, %d, "%s");' %value2
        print(sql_insert1)
        print(sql_insert2)
        try:
            cur.execute(sql_insert1)
            cur.execute(sql_insert2)
            conn.commit()
        except Exception as e:
            print(e)
        i+=1
        
    cur.close()
    conn.close()
    


def weather_to_db():
    f=open(r"weather.json", "r")
    out = f.read()
    tmp = json.dumps(out)
    tmp = json.loads(out)
    f.close()
    
    conn,cur = get_conn_cur()
    
    weather_main = tmp['weather'][0]['main']
    weather_description = tmp['weather'][0]['description']
    temp = tmp['main']['temp']
    feels_like = tmp['main']['feels_like']
    temp_min = tmp['main']['temp_min']
    temp_max = tmp['main']['temp_max'] 
    pressure = tmp['main']['pressure']
    humidity = tmp['main']['humidity']
    visibility = tmp['visibility']
    wind_speed = tmp['wind']['speed']
    wind_deg = tmp['wind']['deg']
    clouds_all = tmp['clouds']['all']
    rain_1h = tmp.get('rain',{}).get('1h',0)
    rain_3h = tmp.get('rain',{}).get('3h',0)
    snow_1h = tmp.get('snow',{}).get('1h',0)
    snow_3h = tmp.get('snow',{}).get('3h',0)
    dt = tmp['dt']
    sunrise = tmp['sys']['sunrise' ]
    sunset = tmp['sys']['sunset' ]
    
    value = (weather_main, weather_description, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, clouds_all, rain_1h, rain_3h, snow_1h, snow_3h, dt, sunrise, sunset)
    sql_insert ="insert into weather(weather_main, weather_description, temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, wind_speed, wind_deg, clouds_all, rain_1h, rain_3h, snow_1h, snow_3h, dt, sunrise, sunset) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');"    
    print(sql_insert % value)
    
    try:   
        cur.execute(sql_insert % value)
        conn.commit()
    except Exception as e:
        print(e)
    
    cur.close()
    conn.close()
    
def get_fotecast(station_id):
        url='http://api.openweathermap.org/data/2.5/forecast?q=Dublin,ie&units=metric&appid=62d8e38e8a3f439885a38dcff6e8e86d'

        try:
            now=datetime.now()
            print('Fotecast:', now)
            text_page=requests.get(url).text
            tmp = json.loads(text_page)['list']
            
        except:
            print (traceback.format_exc())
                
        num = len(tmp)
        i=0
        
        list = []
        time_list=[]
        while i < num:
            dict = {}
            time=datetime.fromtimestamp(tmp[i]['dt']).isoformat()
            dict['weather_main'] = tmp[i]['weather'][0]['main']
            #dict['weather_description'] = tmp[i]['weather'][0]['description']
            dict['temp'] = tmp[i]['main']['temp']
            dict['feels_like'] = tmp[i]['main']['feels_like']
            dict['temp_min'] = tmp[i]['main']['temp_min']
            dict['temp_max'] = tmp[i]['main']['temp_max'] 
            dict['pressure'] = tmp[i]['main']['pressure']
            dict['humidity'] = tmp[i]['main']['humidity']
            #dict['visibility'] = tmp[i].get('visibility',{})
            dict['wind_speed'] = tmp[i]['wind']['speed']
            dict['wind_deg'] = tmp[i]['wind']['deg']
            dict['clouds_all'] = tmp[i]['clouds']['all']
            dict['rain_3h'] = tmp[i].get('rain',{}).get('3h',0)
            dict['snow_3h'] = tmp[i].get('snow',{}).get('3h',0)
            dict['hour'] = datetime.fromtimestamp(tmp[i]['dt']).hour
            dict['weekday'] = datetime.fromtimestamp(tmp[i]['dt']).weekday()
            list.append(dict)
            time_list.append(time)
            i+=1
      
        df = json_normalize(list)
        df['number']= station_id
        
        df = pd.get_dummies(df)   

        
        X_test = pd.read_csv('/X_test.csv')
        
        columns=[]
        for i in X_test.columns:
            if i not in df.columns:
                columns.append(i)
        
        for i in columns:
            df[i]=0

        return df, time_list
        
'''df,time_list=get_fotecast(42)
print(df.dtypes)
print(df)
with open('model.pkl', 'rb') as handle:     
    model = pickle.load(handle)  
print(model.predict(df))
print(time_list)'''




    
    
    
                    