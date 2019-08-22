import discord, textwrap

class snifferbot(discord.Client):
    '''
    Events
    '''

    async def on_connect(self):
        print('Connected')

    async def on_ready(self):
        print('Ready')
        self.guild = self.guilds[0]
        self.channels = {c.name.lower():c for c in self.guild.text_channels}
        self.roles = {r.name.lower():r for r in self.guild.roles}

    async def on_message(self, message):
        if message.author == self.user:
            return

    async def on_message_edit(self, before, after):
        log = textwrap.dedent('''\
                Message edited by {0} in {1}:
                From: ```<{2}> {3}```
                To: ```<{4}> {5}```'''\
                    .format(before.author.mention, before.channel.mention,
                        before.author.name, before.content,
                        after.author.name, after.content))
        await self.post(report, 'log')

    async def on_message_delete(self, message):
        log = textwrap.dedent('''\
                Message deleted by {0} in {1}: ```<{2}> {3}```'''\
                    .format(message.author.mention, message.channel.mention,
                        message.author.name, message.content))
        await self.post(report, 'log')

    async def on_member_join(self, member):
        member.add_roles([self.roles['309mj']])

    async def on_member_remove(self, member):
        if self.roles['mute'] in member.roles:
            await member.ban()
            await self.post('Banning {0} for mute evading.'.format(member.mention), 'log')

        message = '{0} left the server.'.format(member.name)
        await self.post(message, 'reception')

    '''
    Helper Functions
    '''

    async def post(self, message, channel):
        await self.channels[channel].send(message)

    # async def region(self, member, region):

