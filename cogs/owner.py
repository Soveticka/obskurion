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

    # TODO - Currently can handle only Headless clients, needs to be reworked so it can handle Player raids and later all the raids. ideally all embeds.
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
        if name == 'headless':
            path = 'fika/location/raids'
        else: 
            path = 'fika/presence/get'
        data = apiRequests.request_data(apiRequests.build_url('games-windows.lab', 6969, path))

        serverID_Delta = '67e67855afdbd623a800223c'
        serverID_Gamma = '67e67855afdbd623a8002379'

        field_1 = "Server is Idle"
        field_2 = "Server is Idle"

        for raid in data:
            if raid['serverId'] == serverID_Delta:
                field_1 = await self.build_embed(raid, name)
            elif raid['serverId'] == serverID_Gamma:
                field_2 = await self.build_embed(raid, name)
        
        embed.set_field_at(index=0, name="Delta", value=field_1, inline=True)
        embed.set_field_at(index=1, name="Gamma", value=field_2, inline=True)
        print("Changing the embed")
        await message.edit(embed=embed)


    async def build_embed(self, data: dict, mode: str) -> str:
        """Constructs parts of embed depending on the mode -> Can prepare dictionary for each of the parts of Embed.

        Args:
            data (dict): Info needed for the specified part of Embed
            mode (str): Determines what will be constructed

        Returns:
            dict: ready to be used data
        """
        players = fileHandling.loadJson(f'{self.current_dir}/.private_stuff/players.json')
        playersInRaid = ''
        mapList = {
            "bigmap": "Customs",
            "factory4_day": "Factory (Day)",
            "factory4_night": "Factory (Night)",
            "interchange": "Interchange",
            "laboratory": "Labs",
            "rezervbase": "Reserve",
            "shoreline": "Shoreline",
            "woods": "Woods",
            "lighthouse": "Lighthouse",
            "tarkovstreets": "Streets of Tarkov",
            "sandbox": "Ground Zero",
            "sandbox_high": "Ground Zero (21+)"
        }
        if mode == 'headless':
            for player in data['players'].keys():
                #if players.get('players')[player]:
                if player in players.get('players').keys():
                    playersInRaid += players.get('players')[player]['nickname'] + ', '
                continue
            newField = f'Started By: {data['headlessRequesterNickname']}\nFaction: {('SCAV' if data['side'] == 'Savage' else data['side'])}\nMap: {mapList.get(data['location'])}\nTime: {data['time']}\nPlayers: {playersInRaid[:-2]}'
        elif mode == 'player':
            pass
        return newField
    
    @commands.command()
    async def test(self, ctx):
        channel = self.bot.get_channel(1312855728439955516)
        message = await channel.fetch_message(1357450159981854911)
        embed = message.embeds[0]
        print(embed.fields)
