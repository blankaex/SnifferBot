async def help(bot, channel):
    with open(bot.data + 'help', 'r') as help:
        await bot.post_embed(title='Commands:', description=help.read(), channel=channel)
