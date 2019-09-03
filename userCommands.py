#cython: language_level=3

import data
import discord

from discordHelper import User, newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW, ORANGE


async def vouch(user: discord.User,
                targetUser: discord.User,
                message: str,
                curChannel: discord.TextChannel,
                pendingVouchesChannel: discord.TextChannel):
    '''
        Leaves a vouch for a user
    '''
    u = User(user.id)
    if user.id in u.allData['Blacklist']:
        return

    # Clean the message
    isPositive = '-' not in message
    if message[0] == '-' or message[0] == '+':
        message = message[1:].strip()

    # Save to pending vouches
    d = data.loadJSON(data.DATABASE_FILENAME)
    vouchNum: int = d['VouchCount'] + 1
    vouch = {
        'ID': vouchNum,
        'Giver': user.id,
        'Receiver': targetUser.id,
        'IsPositive': isPositive,
        'Message': message,
    }
    pendingVouches: list = d['PendingVouches']
    pendingVouches.append(vouch)
    data.updateJson(data.DATABASE_FILENAME, {
        'PendingVouches': pendingVouches,
        'VouchCount': vouchNum,
    })

    # Send embeds to the user
    embed = newEmbed(description='Vouch is pending.', color=YELLOW)
    embed2 = newEmbed(
        description='Thank you for vouching using our bot, please remember when vouching for someone to state the deal when vouching for someone', color=GREEN)
    await curChannel.send(embed=embed)
    await curChannel.send(embed=embed2)

    # Send embed to pending channel
    embed = newEmbed(description='', title=f'Vouch ID: {vouchNum}')
    embed.add_field(name='Type', value=(
        'Pos' if isPositive else 'Neg'), inline=False)
    embed.add_field(name='Receiver', value=targetUser.name, inline=False)
    embed.add_field(name='Giver', value=user.name, inline=False)
    embed.add_field(name='Comment', value=message, inline=False)
    embed.set_footer(
        text=f'+approve {vouchNum} | +deny {vouchNum} in order to assign this vouch')
    await pendingVouchesChannel.send(embed=embed)


async def redeem(user: discord.User, token: str,
                 channel: discord.TextChannel,
                 logChannel: discord.TextChannel):
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

    if success:
        embed = newEmbed(
            description=f'{user.mention} redeemed their vouches!',
            title='Vouch redeemed!')
        await logChannel.send(embed=embed)


async def link(user: discord.User, link: str, channel: discord.TextChannel):
    '''
        Links a Nulled.to account to the profile
    '''
    u = User(user.id)
    u.setLink(link)
    embed = newEmbed(description='Successfully set profile link!', color=GREEN)
    await channel.send(embed=embed)


async def profile(targetUser: discord.User, bcGuild: discord.Guild,
                  channel: discord.TextChannel):
    '''
        If a user is mentioned, it will display their profiles
        details. If a user isn't mentioned, then the author's
        profile is displayed.
    '''
    u = User(targetUser.id)

    # Decide a proper color
    if u.isScammer:
        color = RED
    elif u.dwc:
        color = ORANGE
    elif u.negVouchCount > u.posVouchCount:
        color = YELLOW
    else:
        color = GREEN

    # Add relevant information
    embed = newEmbed(description='', title='', color=color)
    embed.add_field(name='Vouch Information',
                    value=f'**Positive:** {u.posVouchCount}\n**Negative:** {u.negVouchCount}\n\n**Total:** {len(u.vouches)}')

    # Added Nulled link and verification
    nulledLink = f'[Click Here]({u.link})' if u.link else 'None'
    verification = ''
    if u.link:
        verification = '❌' if not u.verified else '✅'
        verification = f'**Verification:**{verification}\n'

    # Add tags and comments
    embed.add_field(
        name='Tags', value=f'**Scammer:** {u.isScammer}\n**DWC:** {u.dwc}\n{verification}**Nulled Link:** {nulledLink}')

    if u.vouches:
        comments = []
        prevLength = 0
        # Combine all the vouch messages into a list
        for i, x in list(enumerate(u.vouches))[::-1]:
            comment = f'{i+1}) ' + x.message
            # We have to make sure the string total is less than
            # 1024 characters otherwise discord wont send it
            if len(comment) + prevLength <= 1024:
                prevLength += len(comment)
                comments.append(comment)
            else:
                break
        # Combine the comments into new lines
        if comments:
            comments = '\n'.join(comments)
            embed.add_field(name='Comments', value=comments, inline=False)

    # Gather possible roles
    badges = []
    supporter_role = discord.utils.get(
        bcGuild.roles, name='Supporters | Partners')
    staff_role = discord.utils.get(bcGuild.roles, name='VP Staff')
    developer_role = discord.utils.get(bcGuild.roles, name='Developer | Devs')
    owner_role = discord.utils.get(bcGuild.roles, name='Owner | Founder')
    sl_staff_role = discord.utils.get(bcGuild.roles, name='SL Staff')
    trusted_role = discord.utils.get(bcGuild.roles, name='Trusted')

    # Give out proper badges based on roles
    for member in bcGuild.members:
        if member == targetUser:
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

    if u.isScammer:
        authorName = f'💀{str(targetUser)} 💀'
    elif u.dwc:
        authorName = f'⚠️{str(targetUser)} ⚠️'
    else:
        authorName = f'{str(targetUser)}\'s Profile'

    embed.add_field(name='Badges', value=formattedBadges, inline=False)
    embed.set_author(name=authorName, icon_url=targetUser.avatar_url)
    embed.set_thumbnail(url=targetUser.avatar_url)
    embed.set_footer(text='Endorsed by BCN')

    await channel.send(embed=embed)


async def token(user: discord.User, channel: discord.TextChannel):
    u = User(user.id)
    embed = newEmbed(description=f'Your token: {u.token}')
    await user.send(embed=embed)
    embed = newEmbed(description='Token was DM\'d to you.')
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
    embed.add_field(name=f'{prefix}token',
                    value='View your current token.',
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

    await channel.send(embed=embed)


async def about(channel: discord.TextChannel, avatarUrl):
    embed = newEmbed(description='', title='About Vouch Pro')

    embed.add_field(name='What is it?', value=f'**Vouch Pro is a bot created to end the corruption from Vouch Bot.** The owners/staff of Vouch Bot have been found to extort users for their own personal advantage. As a result of this, the owner of BCN, Band1t contracted Reboot Services to create a new Vouch Bot with no corruption. This community-led bot has been paid for not only by the staff of BCN, but also you as a community. This bot has it\'s approval system viewable in public, unlike Vouch Bot which prefers to hide it behind the scenes.')
    embed.add_field(name='How do I add it?',
                    value='**Below is the invite URL:\n**https://discordapp.com/oauth2/authorize?client_id=597631338253778991&scope=bot&permissions=67584')
    embed.set_image(
        url='https://media.discordapp.net/attachments/588968667878785026/588968710648365066/Screenshot_2019-06-13_at_11.41.57_PM.png?width=1395&height=642')
    embed.add_field(name='Proof Of Corruption', value='⬇')
    embed.set_author(name='Vouch Pro', icon_url=avatarUrl)
    embed.set_footer(text='Endorsed by BCN')

    await channel.send(embed=embed)
