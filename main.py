#cython: language_level=3

import data
import config
import discord
import discordCommands

PREFIX = '+'


class DiscordBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

        if loweredMsg.startswith(f'{PREFIX}'):
            pass

        # =====================================================

        elif loweredMsg.startswith(f'{PREFIX}help'):
            await discordCommands.help(PREFIX,
                                       message.channel,
                                       (message.author.id in self.masterIDs))

        # =====================================================


def main():
    DiscordBot().run(config.DISCORD_TOKEN)


if __name__ == '__main__':
    main()
