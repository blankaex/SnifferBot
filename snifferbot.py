import discord

class snifferbot(discord.Client):
    '''
    Events
    '''

    async def on_connect(self):
        print('Connected')

    async def on_ready(self):
        print('Logged on as {0}.'.format(self.user))
        self.guild = self.guilds[0]
        self.channels = {c.name.lower():c for c in self.guild.text_channels}
        self.roles = {r.name.lower():r for r in self.guild.roles}

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print('Message from {0.author}: {0.content}'.format(message))

    async def on_message_edit(self, before, after):
        print('Message from {0.author}: {0.content}'.format(before))

    async def on_message_delete(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

    async def on_member_join(self, member):
        member.add_roles([self.roles['309mj']])

    async def on_member_remove(self, member):
        message = '{0} left the server.'.format(member.name)
        await self.post(message, 'reception')

    '''
    Helper Functions
    '''

    async def post(self, message, channel):
        await self.channels[channel].send(message)
