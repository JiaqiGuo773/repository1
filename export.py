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

csvfile = open('a.csv', 'wb')
writer = csv.writer(csvfile,dialect='excel')
conn,cur = utils.get_conn_cur()
cur.execute("select * from availability")
data=cur.fetchall
writer.writerows(data)
csvfile.close()
conn.commit()
cur.close()
conn.close()
