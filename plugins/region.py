import json, textwrap

async def region(bot, args, author):
    if not bot.roles['309mj'] in author.roles:
        await bot.post('You already have a region.', 'reception')
        return

    with open(bot.data + 'regions', 'r') as r:
        regions = json.load(r)

    region, *_ = args.split(' ', 1) 
    if not region in regions: 
        await bot.post(textwrap.dedent('''\
            Invalid region. Usage: `!region [REGION]`
            Where `[REGION]` is one of `usa`, `can`, `eur`, `asia`, `aus`.
            Example: `!region usa`'''), 'reception')

    else:
        await author.add_roles(bot.roles[regions[region]])
        await author.remove_roles(bot.roles['309mj'])
        await bot.post('Region set.', 'reception')
