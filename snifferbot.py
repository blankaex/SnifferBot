import discord

class snifferbot(discord.Client):
    async def on_connect(self):
        print('Connected')

    async def on_ready(self):
        print('Logged on as {0}.'.format(self.user))
        self.guild = self.guilds[0]
        self.channels = {c.name:c for c in self.guild.text_channels}

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print('Message from {0.author}: {0.content}'.format(message))

    async def on_message_edit(self, before, after):
        print('Message from {0.author}: {0.content}'.format(before))

    async def on_message_delete(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

    async def on_member_join(self, member):
        print('TODO')
        #TODO

    async def on_member_leave(self, member):
        print('TODO')
        #TODO
