import os
from datetime import datetime

from discord import Embed
from discord.ext import commands

from methods import fileHandling
from methods import apiRequests


class Owner(commands.Cog):
    """_summary_

    Args:
        commands (_type_): _description_
    """
    def __init__(self, bot):
        self.bot = bot
        self.current_dir = os.getcwd()

    @commands.command()
    async def generate_embed(self, ctx, name: str) -> None:
        """_summary_

        Args:
            ctx (_type_): _description_
            name (str): _description_
        """
        data = fileHandling.loadJson(f"{self.current_dir}/lists/embeds.json")

        embed = Embed(
            title="Headless Servers", colour=0x00B0F4, timestamp=datetime.now()
        )

        embed.add_field(
            name="{Headless Name}",
            value="Started By: {playerName}\nSide?: {side}\nMap:  {raidMap}\nPlayers: {playerList}",
            inline=True,
        )
        embed.add_field(
            name="{Headless Name}",
            value="Started By: {playerName}\nSide?: {side}\nMap:  {raidMap}\nPlayers: {playerList}",
            inline=True,
        )
        embed.set_footer(text="Obskurion", icon_url="https://slate.dan.onl/slate.png")

        data[name] = {"messageID": ctx.message.id, "channelID": ctx.channel.id}

        fileHandling.saveJson(f"{self.current_dir}/lists/embeds.json", data)
        await ctx.send(embed=embed)

    @commands.command()
    async def edit_embed(self, ctx, name: str) -> None:
        """_summary_

        Args:
            ctx (_type_): _description_
            name (str): _description_
        """
        data = fileHandling.loadJson(f"{self.current_dir}/lists/embeds.json")
        embed_list: dict = data.get(name)
        channel = self.bot.get_channel(int(embed_list['channelID']))
        message = await channel.fetch_message(int(embed_list['messageID']))
        embed = message.embeds[0]
        #data = apiRequests.request_data(apiRequests.build_url('games-windows.lab', 6969, path))
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
},
{
    "serverId": "67e67855afdbd623a8002379",
    "hostUsername": "Gamma",
    "playerCount": 2,
    "status": 2,
    "location": "factory4_day",
    "side": "Savage",
    "time": "CURR",
    "players": {
      "67e67855afdbd623a8002379": False,
      "67911bb000015a3013c4b680": False
    },
    "isHeadless": True,
    "headlessRequesterNickname": "ItchyBalls"
}]
        serverID_Delta = '67e67855afdbd623a800223c'
        serverID_Gamma = '67e67855afdbd623a8002379'

        field_1 = "Server is Idle"
        field_2 = "Server is Idle"

        for raid in data:
            if data['serverId'] == serverID_Delta:
                field_1 = await self.build_embed(raid, 'field')
            elif data['serverId'] == serverID_Gamma:
                field_2 = await self.build_embed(raid, 'field')
        
        embed.set_field_at(index=0, name="Delta", value=field_1, inline=True)
        embed.set_field_at(index=1, name="Gamma", value=field_2, inline=True)
        await message.edit(embed=embed)


    async def build_embed(self, data: dict, mode: str) -> str:
        """Constructs parts of embed depending on the mode -> Can prepare dictionary for each of the parts of Embed.

        Args:
            data (dict): Info needed for the specified part of Embed
            mode (str): Determines what will be constructed

        Returns:
            dict: ready to be used data
        """
        if mode == 'field':
            # TODO Find all map names that are returned by the API and create a dict with them.
            players = fileHandling.loadJson(f'{self.current_dir}/.private_stuff/players.json')
            playersInRaid = ''
            for player in data['players'].keys():
                if players.get('players')[player]:
                    playersInRaid += f'players.get(\'players\')[{player}][\'nickname\'],'
                continue
            newField = f'Started By: {data['headlessRequesterNickname']}\nFaction: {('SCAV' if data['side'] == 'Savage' else data['side'])}\nMap: {data['location']}\nTime: {data['time']}\nPlayers: {playersInRaid[:-1]}'
        return newField
    
    @commands.command()
    async def test(self, ctx):
        channel = self.bot.get_channel(1312855728439955516)
        message = await channel.fetch_message(1357450159981854911)
        embed = message.embeds[0]
        print(embed.fields)
