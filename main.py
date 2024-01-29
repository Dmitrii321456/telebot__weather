import telebot
import requests
import datetime
from pprint import pprint
from settings import API_KEY, BOT_KEY

bot = telebot.TeleBot(BOT_KEY)


def get_weather(city, API_KEY):

    code_to_smile = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
    }

    try:
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru'
        )
        data = r.json()
        pprint(data)

        city = data['name']
        temp_now = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            print('Посмотри на улицу не пойму что там за погода!!')


        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise_timestap = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestap = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        print(f'***{datetime.datetime.now().strftime("%d-%m-%Y %H:%H")}***\n'
              f'Погода в городе: {city}\n'
              f'Температура воздуха: {temp_now}C {wd}\n'
              f'Влажность: {humidity}%\n'
              f'Давление: {pressure}\n'
              f'Скорость ветра: {wind_speed}m/c\n'
              f'Время восхоода: {sunrise_timestap.strftime("%d-%m-%Y %H:%H")}\n'
              f'Время заката: {sunset_timestap.strftime("%d-%m-%Y %H:%H")}\n')

    except Exception as ex:
        print(ex)
        print('Проверьте правильность названия города')

def main():
    city = input('Введите название города: ')
    get_weather(city, API_KEY)

if __name__ == '__main__':
    main()
