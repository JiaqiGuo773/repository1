import utils

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
        contract_name  = tmp[i]['contract_name']
        name = tmp[i]['name']
        address = tmp[i]['address'] 
        position_lat = tmp[i]['position_lat']
        position_lng = tmp[i]['position_lng']
        banking = tmp[i]['banking']
        bonus = tmp[i]['bonus']
        bike_stands = tmp[i]['bike_stands']
        available_bike_stands = tmp[i]['available_bike_stands']
        available_bikes = tmp[i]['available_bikes']
        status = tmp[i]['status'] 
        last_update = tmp[i]['last_update'] 
        
        value1 = (number, contract_name, name, address, position_lat, position_lng, banking, bonus, bike_stands, available_bikes, status)
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
    