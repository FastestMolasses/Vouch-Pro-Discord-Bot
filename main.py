#cython: language_level=3

import data
import config
import discord
import userCommands
import adminCommands

from discordHelper import newEmbed, errorMessage, RED, BLUE, GREEN, YELLOW

PREFIX = '+'
PENDING_VOUCHES_CHANNELID = 612851594345840651


class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.masterIDs = data.loadJSON(data.DATABASE_FILENAME)['Masters']

    async def on_ready(self):
        '''
            Called when the discord bot logs in
        '''
        print(f'{self.user.name} Logged In!')
        print('--------------------\n')

    async def on_message(self, message: discord.Message):
        '''
            Handles all the discord commands
        '''
        # Make sure we don't respond to ourselves
        if message.author == self.user:
            return

        isMaster = message.author.id in self.masterIDs
        loweredMsg = message.content.lower()
        words = loweredMsg.split()

        # =====================================================

        if loweredMsg.startswith(f'{PREFIX}vouch'):
            if len(message.mentions) == 0 or len(words) < 3:
                await errorMessage(f'Please follow this format: {PREFIX}vouch [@user] [+ or -] [message]',
                                   message.channel)
                return

            if message.author.id == message.mentions[0].id:
                await errorMessage('You cannot vouch for yourself.', message.channel)
                return

            vouchMessage = ' '.join(words[2:])
            pendingChannel = self.get_channel(PENDING_VOUCHES_CHANNELID)
            await userCommands.vouch(message.author,
                                     message.mentions[0],
                                     vouchMessage,
                                     message.channel,
                                     pendingChannel)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}dwc') and isMaster:
            if len(message.mentions) == 0:
                await errorMessage(f'Please follow this format: {PREFIX}dwc [@user]',
                                   message.channel)
                return

            await adminCommands.dwc(message.mentions[0], message.channel)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}pending') and isMaster:
            await adminCommands.pending(message.channel, self.get_user)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}reply') and isMaster:
            if len(message.mentions) == 0 or len(words) <= 2:
                await errorMessage(f'Please follow this format: {PREFIX}reply [@user]',
                                   message.channel)
                return

            replyMsg = ' '.join(words[2:])
            await adminCommands.reply(message.mentions[0], replyMsg, message.channel)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}remove') and isMaster:
            if len(message.mentions) == 0 or len(words) < 2:
                await errorMessage(f'Please follow this format:\n{PREFIX}remove [@user]\n**or**\n{PREFIX}remove [@user] [vouch ID]',
                                   message.channel)
                return

            vouchNum = -1
            if len(words) >= 3 and words[2].isdigit():
                vouchNum = int(words[2])
                if vouchNum < 0:
                    await errorMessage('Vouch ID cannot be negative!', message.channel)
                    return

            await adminCommands.remove(message.mentions[0], message.channel, vouchNum)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}token'):
            await userCommands.token(message.author, message.channel)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}admin') and isMaster:
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}redeem'):
            if len(words) <= 1:
                await errorMessage(f'Please follow this format: {PREFIX}redeem [token]',
                                   message.channel)
                return

            await userCommands.redeem(message.author, words[1], message.channel)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}blacklist') and isMaster:
            if len(message.mentions) == 0:
                await errorMessage(f'Please follow this format: {PREFIX}blacklist [@user]',
                                   message.channel)
                return
            await adminCommands.blacklist(message.mentions[0], message.channel)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}approve') and isMaster:
            if len(words) < 2 or not words[1].isdigit():
                await errorMessage(f'Please follow this format: {PREFIX}approve [vouch ID]',
                                   message.channel)
                return

            await adminCommands.approve(int(words[1]), message.channel, self.get_user)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}deny') and isMaster:
            if len(words) < 2 or not words[1].isdigit():
                await errorMessage(f'Please follow this format: {PREFIX}approve [vouch ID]',
                                   message.channel)
                return

            await adminCommands.deny(int(words[1]), message.channel)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}glist') and isMaster:
            await adminCommands.glist(message.channel)

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}help'):
            await userCommands.help(PREFIX,
                                    message.channel,
                                    isMaster)

        # =====================================================


def main():
    DiscordBot().run(config.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
