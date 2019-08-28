import data
import string
import random


def generateToken() -> str:
    return ''.join(random.choices(string.hexdigits, k=16)).upper()


allData = data.loadJSON('database-new.json')
vouchCount = 0
users = []

# Upgrading users
for key, i in allData['Vouches'].items():
    receiverID = int(key)
    pos = i.get('Pos', [])
    neg = i.get('Neg', [])

    if len(neg) != 0:
        continue

    ct = [i.split('||') for i in i.get('Comments', [])]
    messages = [i[0] for i in ct]
    giverIDs = [i[1] for i in ct]

    for index, x in enumerate(giverIDs):
        try:
            giverIDs[index] = int(x)
        except ValueError:
            giverIDs[index] = -1

    vouches = []
    for index, x in enumerate(messages):
        vouches.append({
            'ID': vouchCount,
            'Giver': giverIDs[index],
            'Receiver': receiverID,
            'IsPositive': True,
            'Message': x,
        })
        vouchCount += 1

    print(vouches)
    user = {
        'ID': receiverID,
        'Token': i.get('Token', generateToken()),
        'DWC': i.get('DWC Level', 0) > 0,
        'Vouches': vouches,
        'Link': i.get('Nulled', False),
        'Scammer': i.get('Scammer', False),
        'Verified': i.get('Verified', False),
        'PositiveVouches': len(pos),
        'NegativeVouches': 0,
    }

    if user['Link'] is False:
        user['Link'] = ''

    users.append(user)


# Upgrading pending vouches
pendingVouches = []
for key, i in allData['Pending Vouches'].items():
    vouch = {
        'ID': vouchCount,
        'Giver': int(i.get('Voucher', -1)),
        'Receiver': int(i.get('Vouched', -1)),
        'IsPositive': i.get('Type', 'Pos') == 'Pos',
        'Message': i.get('Comment', ''),
    }
    vouchCount += 1
    pendingVouches.append(vouch)

# {
#     'ID': vouchCount,
#     'Giver': giverIDs[index],
#     'Receiver': receiverID,
#     'IsPositive': True,
#     'Message': x,
# }

data.updateJson('database-new2.json',
                {
                    'VouchCount': vouchCount,
                    'Users': users,
                    'PendingVouches': pendingVouches
                })
