#cython: language_level=3

import data
import discord

from discordHelper import User, Vouch, newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW


async def admin(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Master privileges to mentioned user
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


async def add(user: discord.User,
              targetUser: discord.User,
              message: str,
              isPositive: bool,
              curChannel: discord.TextChannel,
              logChannel: discord.TextChannel):
    '''
        Leaves a vouch for a user
    '''
    u = User(user.id)

    # Create a new vouch
    d = data.loadJSON(data.DATABASE_FILENAME)
    vouchNum: int = d['VouchCount'] + 1
    vouch = {
        'ID': vouchNum,
        'Giver': user.id,
        'Receiver': targetUser.id,
        'IsPositive': isPositive,
        'Message': message,
    }
    vouch = Vouch(vouch)
    u.addVouch(vouch)

    # Message the user when their vouch is approved
    # and only if they haven't opted out of notifications
    if not u.ignoreNotifications:
        vouchType = 'positive' if isPositive else 'negative'
        msg = f'Received a {vouchType} vouch!'

        embed = newEmbed(description=msg, color=(GREEN if isPositive else RED))
        embed.set_footer(
            text='React with ❌ to stop receiving vouch notifications')
        await targetUser.send(embed=embed)

    # Send confirmation message
    embed = newEmbed(
        description=f'Added vouch to {targetUser.mention}', color=GREEN)
    await curChannel.send(embed=embed)

    # Send embed to log channel
    embed = newEmbed(description='', title=f'Vouch ID: {vouchNum}')
    embed.add_field(name='Type', value=(
        'Pos' if isPositive else 'Neg'), inline=False)
    embed.add_field(name='Receiver', value=targetUser.name, inline=False)
    embed.add_field(name='Giver', value=user.name, inline=False)
    embed.add_field(name='Comment', value=message, inline=False)
    embed.set_footer(
        text='Added Vouch')
    await logChannel.send(embed=embed)


async def staff(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles staff privileges to mentioned user
    '''
    masters = data.loadJSON(data.DATABASE_FILENAME)['Staff']
    if targetUser.id in masters:
        masters.remove(targetUser.id)
        embed = newEmbed(description='Removed staff!', color=GREEN)
    else:
        masters.append(targetUser.id)
        embed = newEmbed(description='Added staff!', color=GREEN)

    data.updateJson(data.DATABASE_FILENAME, {'Staff': masters})
    await channel.send(embed=embed)


async def dwc(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Deal With Caution role to mentioned user
    '''
    u = User(targetUser.id)
    u.setDWC(not u.dwc)

    if u.dwc:
        embed = newEmbed(
            description=f'Added DWC to {targetUser.mention}!',
            color=GREEN)
    else:
        embed = newEmbed(
            description=f'Removed DWC for {targetUser.mention}!',
            color=GREEN)

    await channel.send(embed=embed)


async def scammer(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Scammer role to mentioned user
    '''
    u = User(targetUser.id)
    u.setScammer(not u.isScammer)

    if u.isScammer:
        embed = newEmbed(
            description=f'Added Scammer to {targetUser.mention}!',
            color=GREEN)
    else:
        embed = newEmbed(
            description=f'Removed Scammer for {targetUser.mention}!',
            color=GREEN)

    await channel.send(embed=embed)


async def blacklist(targetUserID: int, channel: discord.TextChannel):
    '''
        Toggles the blacklist for the mentioned
        user from vouching other people
    '''
    blacklist: list = data.loadJSON(data.DATABASE_FILENAME)['Blacklist']
    if targetUserID in blacklist:
        blacklist.remove(targetUserID)
        embed = newEmbed(
            description='Removed user from blacklist!', color=GREEN)
    else:
        blacklist.append(targetUserID)
        embed = newEmbed(
            description=f'Added to blacklist!',
            color=GREEN)

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

    success = u.removeVouch(vouchID)

    if success:
        description = 'Successfully removed vouch from profile.'
    else:
        description = f'Vouch #{vouchID} does not exist for this profile.'

    embed = newEmbed(
        description=description, color=(GREEN if success else RED))
    await channel.send(embed=embed)


async def pending(channel: discord.TextChannel, getUser):
    pendingVouches = data.loadJSON(data.DATABASE_FILENAME)['PendingVouches']
    if len(pendingVouches) == 0:
        embed = newEmbed(description='No pending vouches!', color=YELLOW)
        await channel.send(embed=embed)
        return

    ids = ''
    for i in pendingVouches:
        ids += str(i['ID']) + (' | Positive' if i['IsPositive']
                               else ' | Negative') + '\n'
    embed = newEmbed(description=ids, title='Pending vouches')
    await channel.send(embed=embed)

    # for i in pendingVouches:
    #     vouchNum = i['ID']
    #     receiverName = getUser(i['Receiver']).name
    #     giverName = getUser(i['Giver']).name

    #     # Send embed to pending channel
    #     embed = newEmbed(description='', title=f'Vouch ID: {vouchNum}')
    #     embed.add_field(name='Type', value=(
    #         'Pos' if i['IsPositive'] else 'Neg'), inline=False)
    #     embed.add_field(name='Receiver', value=receiverName, inline=False)
    #     embed.add_field(name='Giver', value=giverName, inline=False)
    #     embed.add_field(name='Comment', value=i['Message'], inline=False)
    #     embed.set_footer(
    #         text=f'+approve {vouchNum} | +deny {vouchNum} in order to assign this vouch')
    #     await channel.send(embed=embed)


async def verify(targetUser: discord.User, channel: discord.TextChannel):
    '''
        Toggles Verification for mentioned user
    '''
    u = User(targetUser.id)
    u.setVerified(not u.verified)

    if u.verified:
        embed = newEmbed(
            description=f'Verified {targetUser.mention}!', color=GREEN)
    else:
        embed = newEmbed(
            description=f'Unverified {targetUser.mention}!', color=GREEN)

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

    data.updateJson(data.DATABASE_FILENAME, {'PendingVouches': pendingVouches})
    embed = newEmbed(description=f'Deleted vouch #{vouchID}!', color=GREEN)
    await channel.send(embed=embed)


async def approve(vouchID: int, channel: discord.TextChannel,
                  logChannel: discord.TextChannel, getUser):
    '''
        Approves a vouch
    '''
    # Load the pending vouches
    allData = data.loadJSON(data.DATABASE_FILENAME)
    pendingVouches = allData['PendingVouches']

    # Check if the vouch exists, then delete it
    for i, x in enumerate(pendingVouches):
        if x['ID'] == vouchID:
            # vouch = x
            vouch = Vouch(x)
            del pendingVouches[i]
            break
    else:
        await errorMessage(message=f'Could not find vouch with ID: {vouchID}')
        return

    u = User(vouch.receiverID, allData)
    u.addVouch(vouch)
    receiverUser: discord.User = getUser(vouch.receiverID)
    giverUser: discord.User = getUser(vouch.giverID)

    # Message the user when their vouch is approved
    # and only if they haven't opted out of notifications
    if not u.ignoreNotifications:
        isPositive = vouch.isPositive
        vouchType = 'positive' if isPositive else 'negative'
        msg = f'Received a {vouchType} vouch!'

        embed = newEmbed(description=msg, color=(GREEN if isPositive else RED))
        embed.set_footer(
            text='React with ❌ to stop receiving vouch notifications')
        await receiverUser.send(embed=embed)

    # Save the vouch and send embed
    data.updateJson(data.DATABASE_FILENAME,
                    {'PendingVouches': pendingVouches})

    embed = newEmbed(description=f'Approved vouch #{vouchID}!', color=GREEN)
    await channel.send(embed=embed)

    # Send embed to log channel
    embed = newEmbed(description='', title=f'Vouch ID: {vouchID}')
    embed.add_field(name='Type', value=(
        'Pos' if isPositive else 'Neg'), inline=False)
    embed.add_field(name='Receiver', value=receiverUser.name, inline=False)
    embed.add_field(name='Giver', value=giverUser.name, inline=False)
    embed.add_field(name='Comment', value=vouch.message, inline=False)
    embed.set_footer(
        text='Approved Vouch')
    await logChannel.send(embed=embed)


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
