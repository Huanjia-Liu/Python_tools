import requests
import json
from datetime import datetime, timedelta
from tqdm import tqdm

def weather_output(last_hour, data):
    last = last_hour
    every_day = data
    for every_hour in every_day:
        weather_dic = {}
        temp_datetime = datetime.fromtimestamp(every_hour['expire_time_gmt'] - 7*3600)

        if(temp_datetime.hour == last):
            continue
        last = temp_datetime.hour
        weather_dic['time'] = temp_datetime.strftime("%m/%d/%Y, %H:30:%S")
        weather_dic['tempeature'] = every_hour['temp']
        weather_dic['humidity'] = every_hour['rh']
        weather_dic['pressure'] = every_hour['pressure']
        weather_dic['wind'] = every_hour['wdir']
        weather_dic['wind_speed'] =  every_hour['wspd']
        
        with open('sample.json', 'a+') as outfile:
            json.dump(weather_dic, outfile)
            outfile.write(",")
    return last

date = datetime.strptime('20050101','%Y%m%d')
url_str = "https://api.weather.com/v1/location/EGLC:9:GB/observations/historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e&units=e&startDate="
#url_str = "https://api.weather.com/v1/location/KLGA:9:US/observations/historical.json?apiKey=6532d6454b8aa370768e63d6ba5a832e&units=e&startDate="
url_mid = "&endDate="
last = 0
error_date = []
with open('sample.json', 'w') as outfile:
    outfile.write('{"observations":[')

year = 15


for i in tqdm(range(year*365)):
    date = date + timedelta(days=1)
    date
    date_str = date.strftime('%Y%m%d')
    final_str = url_str + date_str + url_mid + date_str
    response = requests.get(final_str)
    json_file = response.json()
    try:
        every_day_data = json_file['observations']
    except:
        print("\n"+date_str)
        error_date.append(date_str)
    last = weather_output(last,every_day_data)

with open('sample.json', 'r+') as outfile:
    final_data = outfile.read()[:-1] + "]}" 
with open('sample.json', 'w') as outfile:
    outfile.write(final_data)