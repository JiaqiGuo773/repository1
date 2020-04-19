import utils
import requests
import json
import pymysql
import traceback
from datetime import datetime
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
import pandas as pd

f=open(r"availability.json", "r")
out = f.read()
f.close()
tmp = json.dumps(out)
tmp = json.loads(out)
num = len(tmp)
conn,cur = utils.get_conn_cur()
i=0
while i < num:
        number = tmp[i]['number']
        
        
       

        available_bike_stands = tmp[i]['available_bike_stands']
        available_bikes = tmp[i]['available_bikes']
    
        last_update = tmp[i]['last_update'] 
        
        
        value2 = (number, available_bikes, available_bike_stands, last_update)
       
        sql_insert2 ='insert into availability(number, available_bikes, available_bike_stands, last_update) values (%d, %d, %d, "%s");' %value2
        
        print(sql_insert2)
        try:
            cur.execute(sql_insert2)
            conn.commit()
        except Exception as e:
            print(e)
        i+=1
        
cur.close()
conn.close()
    