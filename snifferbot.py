import discord, json, textwrap, random, re

class snifferbot(discord.Client):

    '''
    Events
    '''

    async def on_ready(self):
        await self.initialize()
        # await self.post('Ready', 'log')
        print('Ready')


    async def on_message(self, message):
        await self.handle_message(message)


    async def on_message_edit(self, before, after):
        await self.log('edit', before, after)


    async def on_message_delete(self, message):
        await self.log('delete', message)


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
        with open('data/regions', 'r') as regions:
            self.regions = json.load(regions)


    async def post(self, message, channel):
        await self.channels[channel].send(message)


    async def log(self, type, message, after=None):
        if message.author.name.lower() == 'snifferbot':
            return

        if type == 'edit':
            log = textwrap.dedent('''\
                Message edited by {0} in {1}:
                From: ```<{2}> {3}```
                To: ```<{4}> {5}```'''\
                    .format(message.author.mention, message.channel.mention,
                        message.author.name, message.content,
                        after.author.name, after.content))

        if type == 'delete':
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

        command = message.content.lower()
        channel = message.channel.name.lower()

        if command == '!ping' and author == 'blankaex':
            await self.post('pong', message.channel.name)

        if command.startswith('!region ') and channel == 'reception':
            await self.region(author, command.split()[1])

        if command.startswith('!8ball '):
            await self.eightball(channel)

        if command.startswith('!decide '):
            await self.decide(command, channel)



    '''
    Commands
    '''

    async def region(self, member, region):
        if not self.roles['309mj'] in member.roles:
            await self.post('You already have a region.', 'reception')
            return

        if not region in self.regions:
            await self.post(textwrap.dedent('''\
                Invalid region. Usage: `!region [REGION]`
                Where `[REGION]` is one of `usa`, `can`, `eur`, `asia`, `aus`.
                Example: `!region usa`'''), 'reception')

        else:
            await member.add_roles(self.roles[self.regions[region]])
            await member.remove_roles(self.roles['309mj'])
            await self.post('Region set.', 'reception')


    async def eightball(self, channel):
        with open('data/8ball', 'r') as responses:
            line = random.choice(responses.readlines())
        await self.post(line, channel)


    async def decide(self, command, channel):
        choice = random.choice(re.split(', | or ', command[8:]))
        await self.post(choice, channel)
