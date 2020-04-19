import math
import pandas as pd
import numpy as np
import pickle
import requests
import json
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import pymysql
import utils

def buildModel():
	getCSV()
	df = cleanAndMergeCSV()
	getModel(df)
	

def getCSV():
		
	conn,cur = utils.get_conn_cur()
	cur.execute("select * from weather;")
	weatherdata=cur.fetchall()
	cur.execute("select * from availability;")
	avadata=cur.fetchall()
	
	cur.close()
	conn.close()
	filename='weather.csv'
	with open(filename,mode='w',encoding='utf-8') as f:
	        write = csv.writer(f,dialect='excel')
	        for item in weatherdata:
	            write.writerow(item)
	filename='availability.csv'
	with open(filename,mode='w',encoding='utf-8') as f:
	        write = csv.writer(f,dialect='excel')
	        for item in avadata:
	            write.writerow(item)	

def cleanAndMergeCSV():
	dynamicdata = pd.read_csv('availability.csv', keep_default_na=True, skipinitialspace=True)
	weatherdata = pd.read_csv('weather.csv',  keep_default_na=True, skipinitialspace=True)
	dynamicdata['last_update_date'] = pd.to_datetime(dynamicdata.last_update, unit='ms')
	weekday_List = []
	hour_List = []
	for i in range(len(dynamicdata['last_update_date'])):
		z = dynamicdata.loc[i, 'last_update_date']
		weekday_List.append(z.weekday())
		hour_List.append(z.hour)
	dynamicdata.insert(dynamicdata.columns.tolist().index('last_update_date') + 1, 'weekday', weekday_List)
	dynamicdata.insert(dynamicdata.columns.tolist().index('last_update_date') + 1, 'hour', hour_List)
	del dynamicdata['last_update_date']
	dt_List = []
	for i in range(len(weatherdata['dt'])):
		dt_List.append(int(weatherdata.loc[i, 'dt']))
	for i in range(len(dt_List)):
		dt_List[i] = datetime.datetime.fromtimestamp(dt_List[i])

	weatherdata.insert(weatherdata.columns.tolist().index('dt') + 1, 'dt_date', dt_List)
	del weatherdata['dt']
	del weatherdata['sunrise']
	del weatherdata['sunset']
	del weatherdata['rain_1h']
	del weatherdata['snow_1h']
	weekday_List = []
	hour_List = []
	for i in range(len(weatherdata['dt_date'])):
		z = weatherdata.loc[i, 'dt_date']
		weekday_List.append(z.weekday())
		hour_List.append(z.hour)
	weatherdata.insert(weatherdata.columns.tolist().index('dt_date') + 1, 'weekday', weekday_List)
	weatherdata.insert(weatherdata.columns.tolist().index('dt_date') + 1, 'hour', hour_List)
	del weatherdata['dt_date']
	df = pd.merge(dynamicdata, weatherdata, on = ["hour", "weekday"])
	df = pd.get_dummies(df)
	del df['visibility']
	df = df.groupby(["number", "hour", "weekday"], as_index = False).mean()
	df.dropna(axis=0, how='any', inplace=True)
	return df

def getModel(df):
	result_variable = 'available_bikes'
	X = df[df.columns.difference([result_variable])]
	y = df[result_variable]
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, shuffle=False)

	model = RandomForestRegressor(n_estimators = 10)
	model.fit(X_train,y_train)
	X_test.to_csv('X_test.csv',sep=',',index=False,header=True)
	with open('model.pkl', 'wb') as handle:     
		pickle.dump(model, handle, pickle.HIGHEST_PROTOCOL) 

buildModel()	
