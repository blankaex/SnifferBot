import discord, json, textwrap, time
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
        await self.log_join(member)
        await member.add_roles(self.roles['309mj'])


    async def on_member_remove(self, member):
        await self.log_leave(member)
        await self.check_evade(member)



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


    async def post_embed(self, color=0x2D2D2D, title=None, description=None,
            author=None, icon=None, thumbnail=None, channel='log'):
        embed = discord.Embed(color=color)
        if title or description:
            embed.add_field(name=title, value=description, inline=False)
        if author and icon:
            embed.set_author(name=author, url=discord.Embed.Empty, icon_url=icon)
        if thumbnail:
            embed.set_thumbnail(url=thumbnail)
        embed.set_footer(text=time.ctime())
        await self.channels[channel].send(embed=embed)


    async def log_edit(self, before, after):
        if before.author.name.lower() == 'snifferbot' or before.content == after.content:
            return

        title = 'Message edited by @{0} in #{1}:'.format(before.author.name, before.channel.name)
        description = textwrap.dedent('''\
            **From:**
            {0}
            **To:**
            {1}'''.format(before.content, after.content))
        await self.post_embed(color=0xFFFF40, title=title, description=description, channel='log')


    async def log_delete(self, message):
        if message.author.name.lower() == 'snifferbot':
            return

        title = 'Message deleted by @{0} in #{1}:'.format(message.author.name, message.channel.name)
        await self.post_embed(color=0xFF4040, title=title, description=message.content, channel='log')


    async def log_join(self, member):
        message = '{0} has joined the server'.format(member.name)
        await self.post_embed(color=0x40FF40, author=message, icon=member.avatar_url, channel='reception')


    async def log_leave(self, member):
        message = '{0} has left the server'.format(member.name)
        await self.post_embed(color=0xFF4040, author=message, icon=member.avatar_url, channel='reception')


    async def check_evade(self, member):
        if self.roles['mute'] in member.roles:
            await member.ban()
            message = 'Banning {0} for mute evading.'.format(member.name)
            await self.post_embed(color=0xFF0000, title=message, channel='log')


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
            await self.post_embed(title='Commands:', description=help.read(), channel=channel)


    async def eightball(self, channel):
        with open('data/8ball', 'r') as responses:
             response = random.choice(responses.readlines())
        await self.post(response, channel)


    async def decide(self, args, channel):
        if args:
            choices = re.split(', | or ', args)
            if len(choices) == 1:
                choice = random.choice(['yes', 'no'])
            else:
                choice = random.choice(choices)
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

            url = 'http://translate.google.com/m?hl={1}&sl={0}&q={2}&ie=UTF-8&oe=UTF-8'\
                .format(fromlang, tolang, text)
            r = requests.get(url)
            translation = html.unescape(re.search('<div dir="ltr" class="t0">(.*?)</div>',
                r.text).groups()[0])

            if r.status_code != requests.codes.ok:
                raise APIError

            await self.post(translation, channel)

        except APIError:
            await self.post('API Error.', channel)

        except:
            await self.post('Usage: `!translate [language from] [language to] [text]`', channel)
