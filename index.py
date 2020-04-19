from flask import Flask
import pymysql
from flask import jsonify
from flask.templating import render_template
import pandas as pd
from sqlalchemy import create_engine
import json
import utils
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

app = Flask(__name__) 


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/stations")
def get_stations():
    engine = utils.get_db()
    sql = "select * from station;"    
    rows = engine.execute(sql).fetchall() 
    print('#found {} stations', len(rows)) 
    return jsonify(stations=[dict(row.items()) for row in rows])

@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
    
    engine = utils.get_db()
    df = pd.read_sql_query("select * from availability where number = %(number)s", engine, params={"number":station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')    
    df.set_index('last_update_date', inplace=True)    
    res = df['available_bike_stands'].resample('1d').mean()
    res=res.fillna("0")
    return jsonify(data=json.dumps(list(zip(map(lambda x: x.isoformat(), res.index),  map(lambda x: int(x),res.values)))))
 
@app.route("/station_occupancy_weekly/<int:station_id>")
def get_station_occupancy_weekly(station_id):
    engine = utils.get_db()
    days = ['Mon','Tue','Wed','Thurs', 'Fri', 'Sat', 'Sun']
    df = pd.read_sql_query("select * from availability where number = %(number)s", engine, params={"number": station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')     
    df.set_index('last_update_date', inplace=True)     
    df['weekday'] = df.index.weekday
    mean_available_stands = df[['available_bike_stands', 'weekday']].groupby('weekday').mean()
    mean_available_bikes = df[['available_bikes', 'weekday']].groupby('weekday').mean()         
    
    mean_available_stands.index = days     
    mean_available_bikes.index = days 
    
    
    df = pd.read_sql_query("select * from availability where number = %(number)s", engine, params={"number":station_id})
    df['last_update_date'] = pd.to_datetime(df.last_update, unit='ms')    
    df.set_index('last_update_date', inplace=True) 
       
    mean_available_stands_h = df['available_bike_stands'].resample('1h').mean()
    mean_available_bikes_h = df['available_bikes'].resample('1h').mean()
    
    mean_available_stands_h=mean_available_stands_h.fillna("0")
    mean_available_bikes_h=mean_available_bikes_h.fillna("0")
    
    
    return jsonify(mean_available_stands=list(zip(mean_available_stands.index,map(lambda x: int(x),mean_available_stands.values))), 
                   mean_available_bikes=list(zip(mean_available_bikes.index,map(lambda x: int(x),mean_available_bikes.values))),
                   mean_available_stands_h=list(zip(map(lambda x: x.isoformat(), mean_available_stands_h.index), map(lambda x: int(x),mean_available_stands_h.values))),
                   mean_available_bikes_h=list(zip(map(lambda x: x.isoformat(), mean_available_bikes_h.index), map(lambda x: int(x),mean_available_stands_h.values)))
                   )


@app.route("/predict/<int:station_id>") 
def predict(station_id):
    df, time_list = utils.get_fotecast(station_id)
    print(df)
    with open('./model/model.pkl', 'rb') as handle:     
        model = pickle.load(handle)  
    
    result = model.predict(df).tolist()
    
    return jsonify(list(zip(time_list,result)))
         



if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)

