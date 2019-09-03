import random

async def lart(bot, args, channel, author):
    user = args if args else author.mention
    with open(bot.data + 'larts', 'r') as larts:
        lart = random.choice(larts.readlines()).format(user)
    await bot.post(lart, channel)
