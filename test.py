from methods import apiRequests

path = 'fika/location/raids'
data = apiRequests.request_data(apiRequests.build_url('games-windows.lab', 6969, path))
print(data['serverId'])