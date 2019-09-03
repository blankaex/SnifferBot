import random

async def fortune(bot, channel):
    with open(bot.data + 'fortunes', 'r') as fortunes:
         fortune = random.choice(fortunes.readlines())
    await bot.post(fortune, channel)
