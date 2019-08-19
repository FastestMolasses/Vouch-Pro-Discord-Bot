#cython: language_level=3

import data
import discord

from discordHelper import User, newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW


async def admin():
    '''
        Toggles admin privileges to mentioned user
    '''
    pass


async def dwc(user: discord.User, channel: discord.TextChannel):
    '''
        Toggles Deal With Caution role to mentioned user
    '''
    u = User(user.id)
    u.setDWC(not u.dwc)

    if u.dwc:
        embed = newEmbed(description='Added DWC!', color=RED)
    else:
        embed = newEmbed(description='Removed DWC!', color=GREEN)

    await channel.send(embed=embed)


async def scammer(user: discord.User, channel: discord.TextChannel):
    '''
        Toggles Scammer role to mentioned user
    '''
    u = User(user.id)
    u.setScammer(not u.isScammer)

    if u.dwc:
        embed = newEmbed(description='Added Scammer!', color=RED)
    else:
        embed = newEmbed(description='Removed Scammer!', color=GREEN)

    await channel.send(embed=embed)


async def blacklist():
    '''
        Blacklists the mentioned user from
        vouching other people
    '''
    pass


async def remove():
    '''
        Lists vouches for a person and
        deletes a specific vouch
    '''
    pass


async def deny():
    '''
        Denies a vouch
    '''
    pass


async def approve():
    '''
        Approves a vouch
    '''
    pass


async def reply(targetUser: discord.User, message: str, channel: discord.TextChannel):
    '''
        Sends a message to a user, through the bot
    '''
    try:
        targetUser.send(message)
        embed = newEmbed(description='Sent message!', color=GREEN)
        await channel.send(embed=embed)
    except Exception:
        await errorMessage('Could not send message to user!', channel)


async def glist():
    '''
        Displays all the guilds that the bot is in
    '''
    pass
