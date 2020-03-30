from flask import Flask
import pymysql

app = Flask(__name__) 

conn = pymysql.connect(
            host = 'database-1.cwouctjtnr0b.eu-west-1.rds.amazonaws.com',
            port = 3306,
            user = 'admin',
            passwd = 'jo91TKYJs0czd6DAu4M1',
            db = 'dbikes',)
           
cur = conn.cursor() 

sql = "Select * from station"

a=cur.execute(sql)

@app.route("/")
def hello():
    return a

if __name__ == "__main__":
    app.run(debug=True)

