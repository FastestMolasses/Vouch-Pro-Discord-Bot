#cython: language_level=3

import data
import discord

from discordHelper import User, newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW


async def admin():
    '''
        Toggles admin privileges to mentioned user
    '''
    pass


async def dwc():
    '''
        Toggles Deal With Caution role to mentioned user
    '''
    pass


async def scammer():
    '''
        Toggles Scammer role to mentioned user
    '''
    pass


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


async def reply():
    '''
        Sends a message to a user, through the bot
    '''
    pass


async def glist():
    '''
        Displays all the guilds that the bot is in
    '''
    pass
