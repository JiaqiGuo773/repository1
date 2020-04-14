from flask import Flask
import pymysql
from flask import jsonify
from flask.templating import render_template
import pandas as pd
from sqlalchemy import create_engine
import json
import utils

app = Flask(__name__) 


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/stations")
def get_station():
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
 
@app.route("/test")  
def a():
    URI ="127.0.0.1"
    PORT ="3306"
    DB="mydb"
    USER="root"
    PASSWORD = "abc963215"
    
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER,PASSWORD,URI,PORT,DB),echo=True)
    sql = "select * from station;"    
    rows = engine.execute(sql).fetchall() 
    print('#found {} stations', len(rows))
    print(rows[0])
    print(dir(rows[0]))
    a=rows[0]
    print(a.items())
    
    return jsonify(stations=[dict(row.items()) for row in rows])

if __name__ == "__main__":
    app.run(debug=True)

