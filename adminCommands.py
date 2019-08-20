#cython: language_level=3

import data
import discord

from discordHelper import User, newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW


async def admin(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles admin privileges to mentioned user
    '''
    masters = data.loadJSON(data.DATABASE_FILENAME)['Masters']
    if targetUser.id in masters:
        masters.remove(targetUser.id)
        embed = newEmbed(description='Removed admin!', color=GREEN)
    else:
        masters.append(targetUser.id)
        embed = newEmbed(description='Added admin!', color=GREEN)

    data.updateJson(data.DATABASE_FILENAME, {'Masters': masters})
    await channel.send(embed=embed)


async def dwc(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Deal With Caution role to mentioned user
    '''
    u = User(targetUser.id)
    u.setDWC(not u.dwc)

    if u.dwc:
        embed = newEmbed(description='Added DWC!', color=RED)
    else:
        embed = newEmbed(description='Removed DWC!', color=GREEN)

    await channel.send(embed=embed)


async def scammer(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Scammer role to mentioned user
    '''
    u = User(targetUser.id)
    u.setScammer(not u.isScammer)

    if u.dwc:
        embed = newEmbed(description='Added Scammer!', color=RED)
    else:
        embed = newEmbed(description='Removed Scammer!', color=GREEN)

    await channel.send(embed=embed)


async def blacklist(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles the blacklist for the mentioned
        user from vouching other people
    '''
    blacklist: list = data.loadJSON(data.DATABASE_FILENAME)['Blacklist']
    if targetUser.id in blacklist:
        blacklist.remove(targetUser.id)
        embed = newEmbed(
            description='Removed user from blacklist!', color=GREEN)
    else:
        blacklist.append(targetUser.id)
        embed = newEmbed(description='Added user to blacklist!', color=RED)

    data.updateJson(data.DATABASE_FILENAME, {'Blacklist': blacklist})
    await channel.send(embed=embed)


async def remove(targetUser: discord.User,
                 channel: discord.TextChannel,
                 vouchID: int = -1):
    '''
        Lists vouches for a person and
        deletes a specific vouch
    '''
    u = User(targetUser.id)

    # If a vouch ID wasn't passed in, then list them out
    if vouchID == -1:
        vouches = u.formatVouches()
        if len(vouches) == 0:
            vouches = 'No vouches to show!'
        embed = newEmbed(description=vouches, color=BLUE)
        await channel.send(embed=embed)
        return

    u.removeVouch(vouchID)
    embed = newEmbed(
        description='Successfully removed vouch from profile.', color=GREEN)
    await channel.send(embed=embed)


async def pending(channel: discord.TextChannel, getUser):
    pendingVouches = data.loadJSON(data.DATABASE_FILENAME)['PendingVouches']
    if len(pendingVouches) == 0:
        embed = newEmbed(description='No pending vouches!', color=YELLOW)
        channel.send(embed=embed)
        return

    for i in pendingVouches:
        vouchNum = i['ID']
        receiverName = getUser(i['Receiver']).name
        giverName = getUser(i['Giver']).name

        # Send embed to pending channel
        embed = newEmbed(description='', title=f'Vouch ID: {vouchNum}')
        embed.add_field(name='Type', value=(
            'Pos' if i['IsPositive'] else 'Neg'), inline=False)
        embed.add_field(name='Receiver', value=receiverName, inline=False)
        embed.add_field(name='Giver', value=giverName, inline=False)
        embed.add_field(name='Comment', value=i['Message'], inline=False)
        embed.set_footer(
            text=f'+approve {vouchNum} | +deny {vouchNum} in order to assign this vouch')
        await channel.send(embed=embed)


async def deny(vouchID: int, channel: discord.TextChannel):
    '''
        Denies a vouch
    '''
    # Load the pending vouches
    pendingVouches = data.loadJSON(data.DATABASE_FILENAME)['PendingVouches']
    # Check if it exists, then delete it
    for i, x in enumerate(pendingVouches):
        if x['ID'] == vouchID:
            del pendingVouches[i]
            break
    else:
        await errorMessage(message=f'Could not find vouch with ID: {vouchID}')
        return

    data.updateJson({'PendingVouches': pendingVouches})
    embed = newEmbed(description=f'Deleted vouch #{vouchID}!', color=GREEN)
    await channel.send(embed=embed)


async def approve(vouchID: int, channel: discord.TextChannel, getUserFunc):
    '''
        Approves a vouch
    '''
    # Load the pending vouches
    allData = data.loadJSON(data.DATABASE_FILENAME)
    users = allData['Users']
    pendingVouches = allData['PendingVouches']

    # Check if it exists, then delete it
    for i, x in enumerate(pendingVouches):
        if x['ID'] == vouchID:
            vouch = x
            del pendingVouches[i]
            break
    else:
        await errorMessage(message=f'Could not find vouch with ID: {vouchID}')
        return

    # Add vouch to the user
    receiverID = vouch['Receiver']
    for i, x in enumerate(users):
        if x['ID'] == receiverID:
            users[i]['Vouches'].append(vouch)
            break

    # Message the user when their vouch is approved
    receiverUser: discord.User = await getUserFunc(receiverID)
    isPositive = vouch['IsPositive']
    vouchType = 'positive' if isPositive else 'negative'
    msg = f'Received a {vouchType} vouch!'
    embed = newEmbed(description=msg, color=(GREEN if isPositive else RED))
    await receiverUser.send(embed=embed)

    # Save the vouch and send embed
    data.updateJson({'PendingVouches': pendingVouches, 'Users': users})
    embed = newEmbed(description=f'Approved vouch #{vouchID}!', color=GREEN)
    await channel.send(embed=embed)


async def reply(targetUser: discord.User, message: str, channel: discord.TextChannel):
    '''
        Sends a message to a user, through the bot
    '''
    try:
        await targetUser.send(message)
        embed = newEmbed(description='Sent message!', color=GREEN)
        await channel.send(embed=embed)
    except Exception as e:
        print(e)
        await errorMessage('Could not send message to user!', channel)


async def glist(channel: discord.TextChannel):
    '''
        Displays all the guilds that the bot is in
    '''
    pass
