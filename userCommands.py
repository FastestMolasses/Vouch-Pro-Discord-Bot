#cython: language_level=3

import os
import glob
import data
import string
import random
import discord
import asyncio

from discordHelper import newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW


async def vouch(user: discord.User, mentionedUser:
                discord.User, message: str):
    '''
        Leaves a vouch for a user
    '''
    pass


async def redeem(user: discord.User, token: str):
    '''
        Redeems a token and transfers all vouches
        to the new account
    '''
    # NOTE: CHECK IF USER EXISTS
    pass


async def link(user: discord.User, link: str):
    '''
        Links a Nulled.to account to the profile
    '''
    # NOTE: CHECK IF USER EXISTS
    pass


async def profile(user: discord.User):
    '''
        If a user is mentioned, it will display their profile
        details. If a user isn't mentioned, then the author's
        profile is displayed.
    '''
    # NOTE: CHECK IF USER EXISTS
    pass


async def redeem2(country: str, email: str, key: str,
                  channel: discord.channel, user: discord.User):
    embed = newEmbed(f'{user.mention} Loading...', color=YELLOW)
    sentEmbed = await channel.send(embed=embed)

    while True:
        try:
            # Check if we have the account in stock
            accounts = data.getAccountsStock()
            if accounts.get(country, 0) == 0:
                embed = newEmbed(f'{user.mention} This country is out of stock!',
                                 color=RED,
                                 title='Error')
                await sentEmbed.edit(embed=embed)
                return False, ''

            # Get the account info
            filename = os.path.join(
                data.ACCOUNTS_FOLDERNAME, f'{country}.txt')
            d = data.getLineFromTextFile(filename)
            info = [i.strip() for i in d.split('|')]
            account, city, zipcode = info[0], info[4], info[5]

            if True:
                embed = newEmbed(
                    f'{city}\n{zipcode}', color=GREEN)
                await user.send(embed=embed)
                return True, account
            else:
                data.deleteLineFromTextFile(d, filename)
        except Exception as e:
            print(e)


async def restock(account: str, channel: discord.channel):
    country = [i.strip() for i in account.split('|')][1].upper()
    fileName = os.path.join('', country + '.txt')
    data.saveToTextFile(account, fileName)

    embed = newEmbed(f'Saved account!', color=GREEN)
    await channel.send(embed=embed)


async def help(prefix: str, channel: discord.TextChannel, isMaster: bool = False):
    '''
        Displays all the commands that the user can use
    '''
    embed = discord.Embed(title='Vouch Pro Commands',
                          color=(GREEN if isMaster else BLUE))

    embed.add_field(name=f'{prefix}vouch [@user] [+ or -] [message]',
                    value='Leave a positive or negative vouch for the user.',
                    inline=False)
    embed.add_field(name=f'{prefix}redeem [token]',
                    value='Transfers all the vouches from another account to the current one.',
                    inline=False)
    embed.add_field(name=f'{prefix}link [nulled.to link]',
                    value='Link your Nulled profile.',
                    inline=False)
    embed.add_field(name=f'{prefix}profile **OR** {prefix}profile [@user]',
                    value='See a user\'s profile.',
                    inline=False)

    if isMaster:
        embed.add_field(name=f'{prefix}admin [@user]',
                        value='Toggles admin privelges for the user.',
                        inline=False)
        embed.add_field(name=f'{prefix}dwc [@user]',
                        value='Toggles the DWC tag for the user.',
                        inline=False)
        embed.add_field(name=f'{prefix}scammer [@user]',
                        value='Toggles the Scammer tag for the user',
                        inline=False)
        embed.add_field(name=f'{prefix}blacklist [@user]',
                        value='Blacklists a user from vouching.',
                        inline=False)
        embed.add_field(name=f'{prefix}remove [@user] [vouch ID]',
                        value='Removes a vouch from a user.',
                        inline=False)
        embed.add_field(name=f'{prefix}deny [vouch ID]',
                        value='Denies a vouch.',
                        inline=False)
        embed.add_field(name=f'{prefix}approve [vouch ID]',
                        value='Approves a vouch',
                        inline=False)
        embed.add_field(name=f'{prefix}reply [@user]',
                        value='Sends a message to the user with the bot.',
                        inline=False)
        embed.add_field(name=f'{prefix}glist',
                        value='Displays all the guilds that the bot is in.',
                        inline=False)

    await channel.send(embed=embed)


def generateToken() -> str:
    return ''.join(random.choices(string.hexdigits, k=16)).upper()
