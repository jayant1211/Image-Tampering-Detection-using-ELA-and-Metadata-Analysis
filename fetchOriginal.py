#WEATHER API
#https://archive-api.open-meteo.com/v1/era5?latitude=18.52&longitude=73.86&start_date=2022-07-14&end_date=2022-07-14
#&hourly=weathercode&timezone=Asia%2FBangkok

import urllib
from exif import Image
from urllib.request import urlopen
import json


'''0:	'Clear sky'
1, 2, 3	: 'Mainly clear, partly cloudy, and overcast'
45, 48	Fog and depositing rime fog
51, 53, 55	Drizzle: Light, moderate, and dense intensity
56, 57	Freezing Drizzle: Light and dense intensity
61, 63, 65	Rain: Slight, moderate and heavy intensity
66, 67	Freezing Rain: Light and heavy intensity
71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
77	Snow grains
80, 81, 82	Rain showers: Slight, moderate, and violent
85, 86	Snow showers slight and heavy
95 *	Thunderstorm: Slight or moderate
96, 99 *	Thunderstorm with slight and heavy hail'''
weatherDict = {}
weatherDict[0] = 'Sunny'
for key in [1, 2]:
    weatherDict[key] = 'Clear or partly cloudy'
weatherDict[3] = 'Slight Rain'
for key in [45, 48]:
    weatherDict[key] = 'Fog'
for key in [51, 53, 55,56, 57]:
    weatherDict[key] = 'Slight Raining'
for key in [61, 63, 65,66, 67,80, 81, 82]:
    weatherDict[key] = 'Raining Raining'
for key in [45, 48,71, 73, 75,77,85, 86]:
    weatherDict[key] = 'Snow'
for key in [95,96,99]:
    weatherDict[key] = 'Lightning'

params = {}
base_url = 'https://archive-api.open-meteo.com/v1/era5?'

#https://stackoverflow.com/questions/64113710/extracting-gps-coordinates-from-image-using-python
def decimal_coords(coords, ref):
    decimal_degrees = coords[0] + coords[1] / 60 + coords[2] / 3600
    if ref == "S" or ref =='W' :
        decimal_degrees = -decimal_degrees
    return decimal_degrees

def image_coordinates(image_path):
    with open(image_path, 'rb') as src:
        img = Image(src)
    if img.has_exif:
        try:
            img.gps_longitude
            coords = (decimal_coords(img.gps_latitude,img.gps_latitude_ref),
                      decimal_coords(img.gps_longitude,
                      img.gps_longitude_ref))
        except AttributeError:
            try:
                coords = decimal_coords(img.gps_latitude,"N"),decimal_coords(img.gps_longitude,"N")
            except AttributeError:
                print ('No Coordinates. Please run with ELA only.(outdoor=n)')
                exit()
    else:
        print ('The Image has no EXIF information. Please run with ELA only.(outdoor=n)')
        exit()
    try:
        date_time = img.datetime_original
    except AttributeError:
        try:
            date_time = img.gps_datestamp
            date_time += " 12:00:00"
        except:
            print("Date not Available. Please run with ELA only.(outdoor=n)")
            exit()
    latitude = coords[0]
    longitude = coords[1]
    #print({"imageTakenTime":img.datetime_original, "geolocation_lat":coords[0],"geolocation_lng":coords[1]})
    return date_time,latitude,longitude

#date_time,lat,long = image_coordinates('MetaData/img2.jpg')

def get_weather(date_time,lat,long):
    #2022:12:01 12:09:65
    date = date_time[:10]
    time = date_time[11:]

    date = date.replace(':','-')
    params['Date'] = date
    params['Time'] = time
    params['Longitude'] = long
    params['Latitude'] = lat

    url = base_url + 'latitude={}&longitude={}&start_date={}&end_date={}&hourly=weathercode&timezone=Asia%2FBangkok'.format(params['Latitude'],params['Longitude'],params['Date'],params['Date'])

    response = urlopen(url)
    data_json = json.loads(response.read())

    #print(data_json)
    weather_code = data_json['hourly']['weathercode']
    #print(weather_code)
    hour = int(time[:2])


    return weatherDict[weather_code[hour-1]]





