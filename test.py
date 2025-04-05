from methods import apiRequests

path = 'fika/location/raids'
data = [{
    "serverId": "67e67855afdbd623a800223c",
    "hostUsername": "Delta",
    "playerCount": 2,
    "status": 2,
    "location": "factory4_day",
    "side": "Savage",
    "time": "CURR",
    "players": {
      "67e67855afdbd623a800223c": False,
      "67911bb000015a3013c4b680": False
    },
    "isHeadless": True,
    "headlessRequesterNickname": "ItchyBalls"
}]
print(data[0])

if '67e67855afdbd623a800223c' in data:
    print('works')