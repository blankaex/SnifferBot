import os
from core.messagehandler import *

def initialize(bot):
    # fix this to make it less hacky
    bot.data = os.path.dirname(os.path.abspath(__file__)) + '/../plugins/data/'
    bot.guild = bot.guilds[0]
    bot.channels = {c.name.lower():c for c in bot.guild.text_channels}
    bot.roles = {r.name.lower():r for r in bot.guild.roles}
    bot.emotes = {e.name.lower():e for e in bot.guild.emojis}


async def log_edit(bot, before, after):
    if before.author.name.lower() == 'snifferbot' or before.content == after.content:
        return
    title = 'Message edited by @{0} in #{1}:'.format(before.author.name, before.channel.name)
    description = '**From:**\n{0}\n**To:**\n{1}'.format(before.content, after.content)
    await bot.post_embed(color=0xFFFF40, title=title, description=description, channel='log')


async def log_delete(bot, message):
    if message.author.name.lower() == 'snifferbot':
        return
    title = 'Message deleted by @{0} in #{1}:'.format(message.author.name, message.channel.name)
    await bot.post_embed(color=0xFF4040, title=title, description=message.content, channel='log')


async def log_join(bot, member):
    message = '{0} has joined the server'.format(member.name)
    await bot.post_embed(color=0x40FF40, author=message, icon=member.avatar_url, channel='reception')


async def log_leave(bot, member):
    message = '{0} has left the server'.format(member.name)
    await bot.post_embed(color=0xFF4040, author=message, icon=member.avatar_url, channel='reception')


async def send_welcome(bot, member):
    with open('plugins/data/welcome', 'r') as f:
        await member.send(content=f.read().strip())


async def check_evade(bot, member):
    if bot.roles['mute'] in member.roles:
        await member.ban()
        message = 'Banning {0} for mute evading.'.format(member.name)
        await bot.post_embed(color=0xFF0000, title=message, channel='log')


async def check_jp(bot, payload):
    # refactor to add a check for payload.event_type when discord.py updates to 1.3.0
    if payload.message_id == 618081830914097192 and payload.emoji.name == '🇯🇵':
        user = bot.guild.get_member(payload.user_id)
        await user.add_roles(bot.roles['japanese'])
        if bot.roles['309mj'] in user.roles:
            await user.add_roles(bot.roles['asia'])
            await user.remove_roles(bot.roles['309mj'])
