import data
import random
import string
import discord

RED = 0xEF233C
BLUE = 0x00A6ED
GREEN = 0x3EC300
YELLOW = 0xFFB400
ORANGE = 0xFF7106


class User:
    def __init__(self, userID: int, allData: dict = None):
        self.userID = int(userID)
        self.allData = allData or data.loadJSON(data.DATABASE_FILENAME)
        self.users = self.allData['Users']

        # Find the user in the database
        for i in self.users:
            if userID == i['ID']:
                userData = i
                self.isNewUser = False
                break
        else:
            self.isNewUser = True
            userData = {}

        self.ignoreNotifications = userID in self.allData['NoNotificationIDs']
        self.isMaster = userID in self.allData['Masters']
        self.link = userData.get('Link', '')
        self.dwc = userData.get('DWC', False)
        self.isScammer = userData.get('Scammer', False)
        self.token = userData.get('Token', generateToken())
        self.verified = userData.get('Verified', False)
        # Convert the data to Vouch objects
        self.vouches = [Vouch(i) for i in userData.get('Vouches', [])]
        self.posVouchCount = len([i for i in self.vouches if i.isPositive])
        self.negVouchCount = len(self.vouches) - self.posVouchCount

        if self.isNewUser:
            self.save()

    def addVouch(self, vouch):
        '''
            Adds a vouch to the user and database
        '''
        self.vouches.append(vouch)
        self.save()

    def redeemToken(self, token: str) -> bool:
        '''
            Transfers all previous profile data
            to the current one
        '''
        for i, x in enumerate(self.users):
            if x['Token'] == token:
                # Add all the previous vouches to the current account
                self.vouches.extend([Vouch(i) for i in x.get('Vouches')])
                del self.users[i]
                break
        else:
            return False

        self.save()
        return True

    def setScammer(self, scammer: bool):
        '''
            Sets the user as a scammer or not
        '''
        self.isScammer = scammer
        self.save()

    def setDWC(self, dwc: bool):
        '''
            Sets the Deal With Caution flag on the user
        '''
        self.dwc = dwc
        self.save()

    def setLink(self, link: str):
        '''
            Updates the link of the user
        '''
        self.link = link
        self.save()

    def setVerified(self, verified: bool):
        '''
            Updates the verification of the user
        '''
        self.verified = verified
        self.save()

    def removeVouch(self, vouchID: int) -> bool:
        '''
            Removes a vouch from the user and database
        '''
        for i, x in enumerate(self.vouches):
            if x.vouchID == vouchID:
                del self.vouches[i]
                break
        else:
            return False

        self.save()
        return True

    def formatVouches(self) -> string:
        '''
            Lists the vouches in an organized string
        '''
        vouches = ''
        prevLength = 0
        # Combine all the vouch messages into a list
        for i in self.vouches:
            rate = 'Pos' if i.isPositive else 'Neg'
            s = f'**ID** {i.vouchID} **{rate}** | {i.message}\n'
            # We have to make sure the string total is less than
            # 2048 characters otherwise discord wont send it
            if len(vouches) + prevLength <= 2048:
                prevLength += len(s)
                vouches += s
            else:
                break

        return vouches.strip()

    def save(self):
        '''
            Saves the current user into the database
        '''
        d = {
            'ID': self.userID,
            'Token': self.token,
            'DWC': self.dwc,
            'Vouches': [i.toDict() for i in self.vouches],
            'Link': self.link,
            'Scammer': self.isScammer,
            'Verified': self.verified,
            'PositiveVouches': len([i for i in self.vouches if i.isPositive]),
            'NegativeVouches': len(self.vouches) - self.posVouchCount,
        }

        for i, x in enumerate(self.users):
            if x['ID'] == self.userID:
                self.users[i] = d
                break
        else:
            self.users.append(d)
        data.updateJson(data.DATABASE_FILENAME, {'Users': self.users})


class Vouch:
    def __init__(self, vouchData: dict):
        self.vouchID = vouchData.get('ID', -1)
        self.message = vouchData.get('Message', '')
        self.giverID = vouchData.get('Giver', 0)
        self.receiverID = vouchData.get('Receiver', 0)
        self.isPositive = vouchData.get('IsPositive', True)

    def toDict(self) -> dict:
        '''
            Represents the Vouch object as a dictionary
        '''
        return {
            'ID': self.vouchID,
            'Message': self.message,
            'Giver': self.giverID,
            'Receiver': self.receiverID,
            'IsPositive': self.isPositive,
        }


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


def generateToken() -> str:
    return ''.join(random.choices(string.hexdigits, k=16)).upper()
