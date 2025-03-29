import os
import json

current_dir = os.getcwd()
players = {}

async def loadJson(path: str) -> dict:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f'Error reading json: {e}')

async def buildPlayerList(players: dict, path: str) -> dict:
    for filename in os.listdir(path):
        if filename.endswith('.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
    return dict



try:
    with open(f'{current_dir}\\.private_stuff\\players.json', 'r', encoding='utf-8') as f:
        players = json.load(f)
except (json.JSONDecodeError, IOError) as e:
    print(f'Error reading Player list: {e}')
for filename in os.listdir(f'{current_dir}\\.private_stuff\\profiles'):
    if filename.endswith('.json'):
        file_path = os.path.join(f'{current_dir}\\.private_stuff\\profiles', filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data: dict = json.load(f)
                if data.get('info')['password'] != "" or data.get('info')['username'] == "test":
                    continue
                players[data.get('info')['id']] = {
                    "nickname": data.get('characters')['pmc']['Info']['Nickname'],
                    "scavID": data.get('info')['scavId']
                    }
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error reading {filename}: {e}")

with open(f'{current_dir}\\.private_stuff\\players.json', 'w', encoding='utf-8') as f:
    json.dump(players, f, indent=4, ensure_ascii=False)
