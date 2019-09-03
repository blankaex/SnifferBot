import random

async def eightball(bot, channel):
    with open(bot.data + '8ball', 'r') as responses:
         response = random.choice(responses.readlines())
    await bot.post(response, channel)
