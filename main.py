from bot import *

bot = bot()
with open('token', 'r') as token:
    bot.run(token.read())
