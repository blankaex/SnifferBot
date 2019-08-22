import discord

class bot(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

bot = bot()
with open('token', 'r') as token:
    bot.run(token.read())
