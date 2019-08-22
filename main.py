from snifferbot import *

bot = snifferbot()
with open('token', 'r') as token:
    bot.run(token.read())
