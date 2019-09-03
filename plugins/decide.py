import random, re

async def decide(bot, args, channel):
    if args:
        choices = re.split(', | or ', args)
        if len(choices) == 1:
            choice = random.choice(['yes', 'no'])
        else:
            choice = random.choice(choices)
        await bot.post(choice, channel)
    else:
        await bot.post('Usage: `!decide [CHOICE1] or [CHOICE2] ...`', channel)
