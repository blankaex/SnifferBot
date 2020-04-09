# figure out how to dynamically import all modules
from plugins.currency import *
from plugins.decide import *
from plugins.eightball import *
from plugins.fortune import *
from plugins.help import *
from plugins.lart import *
from plugins.region import *
from plugins.translate import *
from plugins.weather import *

async def handle_message(bot, message):
    author = message.author
    if author == bot.user:
        return

    if not message.content.startswith('!'):
        return

    command, *args = message.content.lower().split(' ', 1)
    args = args[0] if args else None

    channel = message.channel.name.lower()

    if command == '!ping' and bot.roles['admin'] in author.roles:
        await bot.post('pong', channel)

    if command == '!region' and channel == 'reception':
        await region(bot, args, author)

    if command == '!help':
        await help(bot, channel)

    if command == '!8ball':
        await eightball(bot, channel)

    if command == '!cc' or command == '!convert':
        await currency(bot, args, channel)

    if command == '!decide':
        await decide(bot, args, channel)

    if command == '!fortune':
        await fortune(bot, channel)

    if command == '!lart':
        await lart(bot, args, channel, author)

    if command == '!translate':
        await translate(bot, args, channel)

    if command == '!w' or command == '!weather':
        await weather(bot, args, channel)
