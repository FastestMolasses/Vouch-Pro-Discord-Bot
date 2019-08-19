#cython: language_level=3

import data
import config
import discord
import userCommands
import adminCommands

PREFIX = '+'


class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: LOAD IDS
        self.channels = []
        self.masterIDs = []

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

        loweredMsg = message.content.lower()
        words = loweredMsg.split()

        # =====================================================

        if loweredMsg.startswith(f'{PREFIX}vouch'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}dwc'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}pending'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}reply'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}remove'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}token'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}admin'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}redeem'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}blacklist'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}approve'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}deny'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}glist'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}help'):
            await userCommands.help(PREFIX,
                                    message.channel,
                                    (message.author.id in self.masterIDs))

        # =====================================================


def main():
    DiscordBot().run(config.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
