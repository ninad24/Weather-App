import datetime
import json
import urllib.request
import os

def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


def fixTime(time):
    fixed_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return fixed_time

def build_url(city_id):
    id = city_id
    unit = 'metric'
    API_KEY = 'Insert API key here'
    url = 'http://api.openweathermap.org/data/2.5/weather?id='
    full_url = url + str(city_id) + '&mode=json&units=' + unit + '&APPID=' + API_KEY
    return full_url


def GetData(full_url):
    url = urllib.request.urlopen(full_url)
    out = url.read().decode('utf-8')
    raw_api_data = json.loads(out)
    url.close()
    return raw_api_data

def organizeData(raw_api_data):
    data = dict(
        city = raw_api_data.get('name'),
        country = raw_api_data.get('sys').get('country'),
        temp = raw_api_data.get('main').get('temp'),
        min_temp = raw_api_data.get('main').get('temp_min'),
        max_temp = raw_api_data.get('main').get('temp_max'),
        wind_speed = raw_api_data.get('wind').get('speed'),
        wind_dir = raw_api_data.get('wind').get('deg'),
        sunrise = raw_api_data.get('sys').get('sunrise'),
        sunset = raw_api_data.get('sys').get('sunset'),
        weather = raw_api_data.get('weather')[0]['main'],
        date = fixTime(raw_api_data.get('dt'))
    )
    return data

def postData(data):
    print('----------------------------------')
    print('Current Weather in: {} , {}'.format(data['city'],data['country']))
    print('Weather Update: {}'.format(data['date']))
    print('Temperature: {} {} Sky'.format(data['temp'],data['weather']))
    print('Maximum Temp: {} Minimum Temp: {}'.format(data['max_temp'],data['min_temp']))
    print('Wind Speed: {}kmph'.format(data['wind_speed']))
    print('Wind direction: {}'.format(data['wind_dir']))
    print('Sunrise: {}'.format(data['sunrise']))
    print('Sunset: {}'.format(data['sunset']))
    print('----------------------------------')


if __name__ == '__main__':
    try:
       test =  postData(organizeData(GetData(build_url(1275339))))
       notify("Weather Update {}".format(datetime.datetime.now().time()), test)

    except IOError:
        print('No Internet Connection!')
