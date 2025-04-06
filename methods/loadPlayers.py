import os

from methods import fileHandling

current_dir = os.getcwd()


def build_playerlist() -> dict:
    """_summary_

    Args:
        path (str): Path to player profiles

    Returns:
        dict: returns new player dict
    """
    players = fileHandling.loadJson(f"{current_dir}/.private_stuff/players.json")
    for filename in os.listdir(f"{current_dir}/.private_stuff/profiles"):
        if filename.endswith(".json"):
            file_path = os.path.join(f"{current_dir}/.private_stuff/profiles", filename)
            data = fileHandling.loadJson(file_path)
            if data.get("info")["password"] != "" or data.get("info")["username"] == "test":
                continue
            players["players"][data.get("info")["id"]] = {
                "nickname": data.get("characters")["pmc"]["Info"]["Nickname"],
                "scavID": data.get("info")["scavId"],
            }
    return players
