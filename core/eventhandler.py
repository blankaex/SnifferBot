import discord, time
import core.helper as helper

class event_handler(discord.Client):

    '''
    Events
    '''

    async def on_ready(self):
        helper.initialize(self)
        await self.post('Ready', 'dev')


    async def on_message(self, message):
        await helper.handle_message(self, message)


    async def on_message_edit(self, before, after):
        await helper.log_edit(self, before, after)


    async def on_message_delete(self, message):
        await helper.log_delete(self, message)


    async def on_member_join(self, member):
        await helper.log_join(self, member)
        await helper.send_welcome(self, member)
        await member.add_roles(self.roles['309mj'])


    async def on_member_remove(self, member):
        await helper.log_leave(self, member)
        await helper.check_evade(self, member)


    async def on_raw_reaction_add(self, payload):
        await helper.check_jp(self, payload)


    '''
    API
    '''

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
