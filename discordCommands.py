#cython: language_level=3

import os
import glob
import data
import string
import random
import discord
import asyncio

RED = 0xEF233C
BLUE = 0x00A6ED
GREEN = 0x3EC300
YELLOW = 0xFFB400


async def redeem(country: str, email: str, key: str,
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


async def help(prefix: str, channel: discord.TextChannel):
    embed = discord.Embed(title='Vouch Pro Commands', color=BLUE)

    embed.add_field(name=f'{prefix}',
                    value='',
                    inline=False)
    embed.add_field(name=f'{prefix}',
                    value='',
                    inline=False)
    embed.add_field(name=f'{prefix}',
                    value='',
                    inline=False)

    await channel.send(embed=embed)


async def errorMessage(message: str, channel: discord.TextChannel):
    embed = newEmbed(message, color=RED, title='Error')
    await channel.send(embed=embed)


def generateToken() -> str:
    return ''.join(random.choices(string.hexdigits, k=16)).upper()


def newEmbed(description: str,
             color: hex = BLUE,
             title: str = 'Vouch Pro') -> discord.Embed:
    return discord.Embed(
        title=title,
        description=description,
        color=color,
    )
