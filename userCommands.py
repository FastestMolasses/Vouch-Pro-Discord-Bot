#cython: language_level=3

import os
import glob
import data
import string
import random
import discord
import asyncio

from discordHelper import User, newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW


async def vouch(user: discord.User, mentionedUser:
                discord.User, message: str):
    '''
        Leaves a vouch for a user
    '''
    # TODO: CHECK BLACKLIST FIRST
    # Send embed to channel
    pass


async def redeem(user: discord.User, token: str, channel: discord.TextChannel):
    '''
        Redeems a token and transfers all vouches
        to the new account
    '''
    u = User(user.id)
    success = u.redeemToken(token)
    if success:
        embed = newEmbed(description='Retrieved all vouches!',
                         title='Token Redeemed', color=GREEN)
    else:
        embed = newEmbed(description='Could not find token!',
                         title='Error', color=RED)

    await channel.send(embed=embed)


async def link(user: discord.User, link: str, channel: discord.TextChannel):
    '''
        Links a Nulled.to account to the profile
    '''
    u = User(user.id)
    if 'nulled.to' not in link:
        errorMessage('Please provide a proper nulled.to link!', channel)
        return

    u.setLink(link)
    embed = newEmbed(description='Successfully set profile link!', color=GREEN)
    await channel.send(embed=embed)


async def profile(user: discord.User, bcGuild: discord.Guild,
                  channel: discord.TextChannel):
    '''
        If a user is mentioned, it will display their profiles
        details. If a user isn't mentioned, then the author's
        profile is displayed.
    '''
    u = User(user.id)

    embed = newEmbed(title=f'{user.name}\'s Profile', color=(
        RED if u.isScammer else GREEN))
    embed.add_field(name='Vouch Information',
                    value=f'**Positive:** {u.posVouchCount}\n**Negative:** {u.negVouchCount}\n\n**Total:** {len(u.vouches)}')
    embed.add_field(
        name='Tags', value=f'**Scammer:** {u.isScammer}\n**DWC:** {u.dwc}\n**Nulled Link:** [Click Here]({u.link})')
    comments = '\n'.join(f'{i+1}{x.message}' for i, x in enumerate(u.vouches))
    print(comments)
    embed.add_field(name='Comments', value=comments, inline=False)
    embed.set_footer(text='Endorsed by BCN')

    badges = []
    # bcGuild = self.bot.get_guild(583416004974084107)
    supporter_role = discord.utils.get(
        bcGuild.roles, name='Supporters | Partners')
    staff_role = discord.utils.get(bcGuild.roles, name='VP Staff')
    developer_role = discord.utils.get(bcGuild.roles, name='Developer | Devs')
    owner_role = discord.utils.get(bcGuild.roles, name='Owner | Founder')
    sl_staff_role = discord.utils.get(bcGuild.roles, name='SL Staff')
    trusted_role = discord.utils.get(bcGuild.roles, name='Trusted')

    for member in bcGuild.members:
        if member == user:
            if owner_role in member.roles:
                badges.append(
                    '<:gem:5987915527222722861>**Owner**<:gem:598791552722272286>')
            if supporter_role in member.roles:
                badges.append(
                    '<:beginner:598389073807278091>**Supporter**<:beginner:598389073807278091>')
            if staff_role in member.roles:
                badges.append(
                    '<:beginner:598389073807278091>**Vouch Pro Staff**<:beginner:598389073807278091>')
            if developer_role in member.roles:
                badges.append(
                    '<:beginner:598389073807278091>**Developer**<:beginner:598389073807278091>')
            if sl_staff_role in member.roles:
                badges.append(
                    '<:beginner:598389073807278091>**SL Staff**<:beginner:598389073807278091>')
            if trusted_role in member.roles:
                badges.append(
                    '<:star2:598788570437779495>**Trusted**<:star2:598788570437779495>')

    formattedBadges = '\n'.join(badges)
    if len(badges) == 0:
        formattedBadges = 'No badges given.'

    embed.add_field(name='Badges', value=formattedBadges, inline=False)
    embed.set_author(name=str(user.id), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)

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
