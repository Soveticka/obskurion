from array import array
from discord.ext import commands
from discord import Embed
import requests
import urllib3

urllib3.disable_warnings()


class Tarkov(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def build_url(self, address: str, port:int, path: str) -> str:
        """Used to build correct API Url.

        Args:
            address (str): Contains domain of the server
            port (int): Server port
            path (str): Path to the endpoint. Without '/' as the first letter.

        Returns:
            str: API Url
        """
        return f'https://{address}:{port}/{path}'
    
    async def request_data(self, url: str) -> array:
        """_summary_

        Args:
            url (str): _description_

        Returns:
            array: _description_
        """
        headers = {
            "responsecompressed": '0'
        }

        try:
            response = requests.get(url, headers=headers, verify=False)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error occured: {e}")

    async def build_embed(playerJson: array, raidData: array, headless = False) -> Embed:
        """_summary_

        Args:
            playerJson (array): _description_
            raidData (array): _description_
            headless (bool, optional): _description_. Defaults to False.

        Returns:
            Embed: _description_
        """
        for raid in raidData:
            for player in playerJson:
                    return
    
    @commands.command()
    async def json(self, message, path):
        """_summary_

        Args:
            message (_type_): _description_
            path (_type_): _description_
        """
        json = await self.request_data(await self.build_url('games-windows.lab', 6969, path))
        print(json)