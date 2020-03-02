import requests, re

async def currency(bot, args, channel):
    amount, *c = re.split(' TO | ', args.upper())
    conversion = c[0] + '_' + c[1]
    url = 'https://free.currconv.com/api/v7/convert'
    with open('tokens/currency') as t:
        token = t.read().strip()
    params = {'q': conversion, 'compact': 'ultra', 'apiKey': token}
    d = requests.get(url, params=params).json()
    try:
        result = float(d[conversion]) * float(amount)
        await bot.post('{} {} = {} {}'.format(amount, c[0], result, c[1]), channel)
    except:
        await bot.post('Error.')
