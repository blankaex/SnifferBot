import discord, textwrap

class snifferbot(discord.Client):

    '''
    Events
    '''

    async def on_ready(self):
        await self.initialize()
        await self.post('Ready', 'dev')
        print('Ready')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.lower().startswith('!region '):
            await self.region(message)

    async def on_message_edit(self, before, after):
        await self.log('edit', before, after)

    async def on_message_delete(self, message):
        await self.log('delete', message)

    async def on_member_join(self, member):
        await member.add_roles([self.roles['309mj']])

    async def on_member_remove(self, member):
        await self.check_evade()
        await self.post('{0} left the server.'.format(member.name), 'reception')


    '''
    Helper Functions
    '''

    async def initialize(self):
        self.guild = self.guilds[0]
        self.channels = {c.name.lower():c for c in self.guild.text_channels}
        self.roles = {r.name.lower():r for r in self.guild.roles}

    async def post(self, message, channel):
        await self.channels[channel].send(message)

    async def check_evade(self, member):
        if self.roles['mute'] in member.roles:
            await member.ban()
            await self.post('Banning {0} for mute evading.'.format(member.mention), 'log')

    async def log(self, type, message, after=None):
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

    async def region(self, message):
        # if message.channel != self.channels['reception']:
        #     return
        member = message.author
        region = message.content.split()[1]
        await self.post(region, 'log')
