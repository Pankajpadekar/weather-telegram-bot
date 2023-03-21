import os
import telebot
import requests
from dotenv import load_dotenv

#load .env file
load_dotenv('config.env', override=True)
bot_token = os.getenv("api_key")
bot = telebot.TeleBot(bot_token)


def get_weather(city):
    api_key_info = os.getenv("user_api")
    url = "http://api.weatherapi.com/v1/current.json?key=" + str(api_key_info) +"&q="+str(city)
    try:
        api_link = requests.get(url)
        api_data = api_link.json()
        api_data['status']=api_link.status_code
    except:
        api_data['status']=api_link.status_code
    return api_data


#start command (/start)
@bot.message_handler(commands=['start'])
def start(message):

    bot_msg = "Hi there , Please Enter /weather_info {Your city name} to get weather info. "

    bot.send_message(message.chat.id , bot_msg)


#weather information command (/weather_info)
@bot.message_handler(commands=['weather_info'])
def weather_info(message ):
    user_message = message.text
    api_data = get_weather(user_message)
    if api_data['status'] == 200:
        response = f'''
            The current weather in 
{api_data['location']['name']},
{api_data['location']['region']}, 
{api_data['location']['country']}
{api_data['location']['localtime']}

--------------**************--------------
    
Weather Condition :      {api_data['current']['condition']['text']}
Temperture city in °C :  {api_data['current']['temp_c']}
Temperture city in °F :   {api_data['current']['temp_f']}
Humidity :                     {api_data['current']['humidity']}
Wind speed in Mph :    {api_data['current']['wind_mph']}
Wind speed in Kph :    {api_data['current']['wind_kph']}


Disclaimer :- If you do not get actual city info which you have entered , try to add country also besides city   
name.'''   

    elif len(user_message) == 0:
        response = "You didn't entry city name , Please try again."

          
    else:
       response = " City not found. Please enter city name correctly. "

    bot.send_message(message.chat.id  , response)
    
    
bot.polling(0.5)
    
