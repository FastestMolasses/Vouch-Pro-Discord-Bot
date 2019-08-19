import data
import discord

RED = 0xEF233C
BLUE = 0x00A6ED
GREEN = 0x3EC300
YELLOW = 0xFFB400


class User:
    def __init__(self, userID: str):
        self.userID = userID
        self.vouches = self.getVouches()
        self.posVouchCount = len(i for i in self.vouches if i.isPositive)
        self.negVouchCount = len(self.vouches) - self.posVouchCount

    def addVouch(self, vouchData: dict):
        '''
            Adds a vouch to the user and database
        '''
        pass

    def removeVouch(self, vouchID: str):
        '''
            Removes a vouch from the user and database
        '''
        pass

    def save(self):
        '''
            Saves the current user into the database
        '''
        pass

    def getVouches(self) -> list:
        '''
            Gets the vouches for the given user, and
            returns a list of Vouch objects
        '''
        pass


class Vouch:
    def __init__(self, vouchData: dict):
        self.vouchID = vouchData.get('vouchID', '')
        self.message = vouchData.get('message', '')
        self.giverID = vouchData.get('giverID', '')
        self.receiverID = vouchData.get('receiverID', '')
        self.isPositive = vouchData.get('isPositive', True)


async def errorMessage(message: str, channel: discord.TextChannel):
    '''
        Sends an error message to a channel
    '''
    embed = newEmbed(message, color=RED, title='Error')
    await channel.send(embed=embed)


def newEmbed(description: str,
             color: hex = BLUE,
             title: str = 'Vouch Pro') -> discord.Embed:
    '''
        Creates a new Embed object
    '''
    return discord.Embed(
        title=title,
        description=description,
        color=color,
    )
