from array import array
from discord.ext import commands
from discord import Embed
import requests
import urllib3

urllib3.disable_warnings()

class Tarkov(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def buildUrl(self, address: str, port:int, path: str) -> str:
        """Used to build correct API Url.

        Args:
            address (str): Contains domain of the server
            port (int): Server port
            path (str): Path to the endpoint. Without '/' as the first letter.

        Returns:
            str: API Url
        """
        return f'https://{address}:{port}/{path}'
    
    async def requestData(self, url: str) -> array:
        headers = {
            "responsecompressed": '0'
        }

        try:
            response = requests.get(url, headers=headers, verify=False)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error occured: {e}")

    async def buildEmbed(playerJson: array, raidData: array, headless = False) -> Embed:
            for raid in raidData:
                 for player in playerJson:
                    return
    
    @commands.command()
    async def json(self, message, path):
        json = await self.requestData(await self.buildUrl('games-windows.lab', 6969, path))
        print(json)