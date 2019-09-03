import requests, textwrap

async def weather(bot, city, channel):
    if isinstance(city, list):
        raise CityNotFound

    url = 'https://api.openweathermap.org/data/2.5/weather'
    with open('tokens/weather') as w:
        token = w.read().strip()
    params = {'q': city, 'appid': token, 'units': 'metric'}

    try:
        d = requests.get(url, params=params).json()

        if d['cod'] == '404' and d['message'] == 'city not found':
            raise CityNotFound
        if d['cod'] == '429':
            raise APILimitExceeded

        cond = d['weather'][0]['main']
        temp = d['main']['temp']
        tempf = round(9 * temp / 5.0 + 32, 2)
        humi = d['main']['humidity']
        wind = d['wind']['speed']
        windm = round(wind * 2.237, 1)

        title = 'Current weather in {0}, {1}:'.format(d['name'], d['sys']['country'])
        description = textwrap.dedent('''\
            **Conditions:** {0} ::  \
            **Temperature:** {1}°C | {2}°F ::  \
            **Humidity:** {3}%  ::  \
            **Wind:** {4}m/s | {5}mph\
            '''.format(cond, temp, tempf, humi, wind, windm))
        await bot.post_embed(title=title, description=description, channel=channel)

    except Exception as CityNotFound:
        await bot.post('City not found.', channel)

    except Exception as APILimitExceeded:
        await bot.post('API limit exceeded. Try again tomorrow', channel)

    except:
        await bot.post('API error.', channel)
