import requests
import datetime
import asyncio
from telebot.async_telebot import AsyncTeleBot

from settings import BOT_KEY, API_KEY

bot = AsyncTeleBot(BOT_KEY)

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Привет! Я телеграм бот который поможет тебе узнать прогноз погоды в любом городе!
Введи название города.\
""")

@bot.message_handler(func=lambda message: True)
async def get_weather(message):
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
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={API_KEY}&units=metric&lang=ru'
        )
        data = r.json()

        city = data['name']
        temp_now = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            await bot.reply_to(message, 'Посмотри на улицу не пойму что там за погода!!')

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        sunrise_timestap = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestap = datetime.datetime.fromtimestamp(data['sys']['sunset'])

        await bot.reply_to(message, f'***{datetime.datetime.now().strftime("%d-%m-%Y %H:%H")}***\n'
              f'Погода в городе: {city}\n'
              f'Температура воздуха: {temp_now}C {wd}\n'
              f'Влажность: {humidity}%\n'
              f'Давление: {pressure}\n'
              f'Скорость ветра: {wind_speed}m/c\n'
              f'Время восхоода: {sunrise_timestap.strftime("%d-%m-%Y %H:%H")}\n'
              f'Время заката: {sunset_timestap.strftime("%d-%m-%Y %H:%H")}\n')

    except Exception as ex:
        print(ex, 'Неправильно введено название города')
        await bot.reply_to(message, 'Проверьте правильность названия города')


if __name__ == '__main__':
    asyncio.run(bot.polling())



