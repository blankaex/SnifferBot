import discord

class snifferbot(discord.Client):
    async def getChannel(self, channel):
        print('TODO')
        #TODO

    async def post(self, channel, message):
        print('TODO')
        #TODO

    async def on_connect(self):
        print('Connected')

    async def on_ready(self):
        print('Logged on as {0}.'.format(self.user))

    async def on_message(self, message):
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
