#cython: language_level=3

import os
import glob
import data
import string
import random
import discord
import asyncio
import discordHelper


async def admin():
    '''
        Gives admin privileges to mentioned user
    '''
    pass


async def dwc():
    '''
        Gives Deal With Caution role to mentioned user
    '''
    pass


async def scammer():
    '''
        Gives Scammer role to mentioned user
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
