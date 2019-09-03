import html, json, re, requests

async def translate(bot, args, channel):
    try:
        fromlang, tolang, text = re.split(' to |, | ', args, 2)

        with open(bot.data + 'languages', 'r') as languages:
            l = json.load(languages)
        
        if not fromlang in l.values():
            fromlang = l[fromlang]

        if not tolang in l.values():
            tolang = l[tolang]

        url = 'http://translate.google.com/m'
        params = {'sl': fromlang, 'hl': tolang, 'q': text, 'ie': 'UTF-8', 'oe': 'UTF-8'}
        r = requests.get(url, params=params)
        translation = html.unescape(re.search('<div dir="ltr" class="t0">(.*?)</div>',
            r.text).groups()[0])

        if r.status_code != requests.codes.ok:
            raise APIError

        await bot.post(translation, channel)

    except KeyError:
        await bot.post('Invalid language.', channel)

    except Exception as APIError:
        await bot.post('API error.', channel)

    except:
        await bot.post('Usage: `!translate [language from] [language to] [text]`', channel)
