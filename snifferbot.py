import discord, json, textwrap
import random, re, requests, html

class snifferbot(discord.Client):

    '''
    Events
    '''

    async def on_ready(self):
        await self.initialize()
        await self.post('Ready', 'log')


    async def on_message(self, message):
        await self.handle_message(message)


    async def on_message_edit(self, before, after):
        await self.log_edit(before, after)


    async def on_message_delete(self, message):
        await self.log_delete(message)


    async def on_member_join(self, member):
        await member.add_roles(self.roles['309mj'])


    async def on_member_remove(self, member):
        await self.check_evade(member)
        await self.post('{0} left the server.'.format(member.name), 'reception')



    '''
    Helper Functions
    '''

    async def initialize(self):
        self.guild = self.guilds[0]
        self.channels = {c.name.lower():c for c in self.guild.text_channels}
        self.roles = {r.name.lower():r for r in self.guild.roles}
        self.emotes = {e.name.lower():e for e in self.guild.emojis}
        with open('data/regions', 'r') as regions:
            self.regions = json.load(regions)


    async def post(self, message, channel):
        await self.channels[channel].send(message)


    async def log_edit(self, before, after):
        if before.author.name.lower() == 'snifferbot' or before.content == after.content:
                return

        log = textwrap.dedent('''\
            Message edited by {0} in {1}:
            From: ```<{2}> {3}```To: ```<{4}> {5}```'''\
                .format(before.author.mention, before.channel.mention,
                    before.author.name, before.content,
                    after.author.name, after.content))

        await self.post(log, 'log')


    async def log_delete(self, message):
        if message.author.name.lower() == 'snifferbot':
                return

        log = textwrap.dedent('''\
            Message deleted by {0} in {1}: ```<{2}> {3}```'''\
                .format(message.author.mention, message.channel.mention,
                    message.author.name, message.content))

        await self.post(log, 'log')


    async def check_evade(self, member):
        if self.roles['mute'] in member.roles:
            await member.ban()
            await self.post('Banning {0} for mute evading.'.format(member.mention), 'log')


    async def handle_message(self, message):
        author = message.author
        if author == self.user:
            return

        command, *args = message.content.lower().split(' ', 1)
        args = args[0] if args else None

        channel = message.channel.name.lower()

        if command == '!ping' and self.roles['admin'] in author.roles:
            await self.post('pong', channel)

        if command == '!region' and channel == 'reception':
            await self.region(args, author)

        if command == '!help':
            await self.help(channel)

        if command == '!8ball':
            await self.eightball(channel)

        if command == '!decide':
            await self.decide(args, channel)

        if command == '!fortune':
            await self.fortune(channel)

        if command == '!lart':
            await self.lart(args, channel, author)

        if command == '!translate':
            await self.translate(args, channel)



    '''
    Commands
    '''

    async def region(self, args, author):
        if not self.roles['309mj'] in author.roles:
            await self.post('You already have a region.', 'reception')
            return

        region, *_ = args.split(' ', 1)
        if not region in self.regions:
            await self.post(textwrap.dedent('''\
                Invalid region. Usage: `!region [REGION]`
                Where `[REGION]` is one of `usa`, `can`, `eur`, `asia`, `aus`.
                Example: `!region usa`'''), 'reception')

        else:
            await author.add_roles(self.roles[self.regions[region]])
            await author.remove_roles(self.roles['309mj'])
            await self.post('Region set.', 'reception')


    async def help(self, channel):
        with open('data/help', 'r') as help:
            await self.post(help.read(), channel)


    async def eightball(self, channel):
        with open('data/8ball', 'r') as responses:
             response = random.choice(responses.readlines())
        await self.post(response, channel)


    async def decide(self, args, channel):
        if args:
            choice = random.choice(re.split(', | or ', args))
            await self.post(choice, channel)
        else:
            await self.post('Usage: `!decide [CHOICE1] or [CHOICE2] ...`', channel)


    async def fortune(self, channel):
        with open('data/fortunes', 'r') as fortunes:
             fortune = random.choice(fortunes.readlines())
        await self.post(fortune, channel)


    async def lart(self, args, channel, author):
        user = args if args else author.mention
        with open('data/larts', 'r') as larts:
            lart = random.choice(larts.readlines()).format(user)
        await self.post(lart, channel)


    async def translate(self, args, channel):
        try:
            fromlang, tolang, text = re.split(' to |, | ', args, 2)

            with open('data/languages', 'r') as languages:
                l = json.load(languages)
            
            if not fromlang in l.values():
                fromlang = l[fromlang]

            if not tolang in l.values():
                tolang = l[tolang]

            try:
                url = 'http://translate.google.com/m?hl={1}&sl={0}&q={2}&ie=UTF-8&oe=UTF-8'\
                    .format(fromlang, tolang, text)
                r = requests.get(url)
                translation = html.unescape(re.search('<div dir="ltr" class="t0">(.*?)</div>',
                    r.text).groups()[0])

                await self.post(translation, channel)

            except:
                await self.post('API Error.', channel)

        except:
            await self.post('Usage: `!translate [language from] [language to] [text]`', channel)
