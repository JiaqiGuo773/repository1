import utils
import time

utils.create_availability()
utils.create_weather()

count = 0

while True:
    
    utils.create_station()
    utils.jcd_file()
    utils.jcd_to_db()
    
    if count % 12 == 0:
        utils.weather_file()
        utils.weather_to_db()
    
    count+=1
    time.sleep(5*60)
    