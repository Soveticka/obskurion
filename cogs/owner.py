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
    async def edit_embed(self, ctx, name: str, path: str) -> None:
        """_summary_

        Args:
            ctx (_type_): _description_
            name (str): _description_
        """
        data = fileHandling.loadJson(f"{self.current_dir}/lists/embeds.json")
        embed_list: dict = data.get(name)
        channel = self.bot.get_channel(embed_list['channelID'])
        message = await channel.fetch_message(embed_list['messageID'])
        embed = message.embeds[0]
        data = apiRequests.request_data(apiRequests.build_url('games-windows.lab', 6969, path))
        # TODO Figure out logic -> If headless is not active update the field with "Idle". If it is used, update the field with data from "build_embed"

        return

    async def build_embed(self, data: dict, mode: str) -> dict:
        """Constructs parts of embed depending on the mode -> Can prepare dictionary for each of the parts of Embed.

        Args:
            data (dict): Info needed for the specified part of Embed
            mode (str): Determines what will be constructed

        Returns:
            dict: ready to be used data
        """
        if mode == 'field':
            # TODO Find all names that are returned by the API and create a dict with them.
            players = fileHandling.loadJson(f'{self.current_dir}/.private_stuff/players.json')
            playersInRaid = ''
            for player in data['players'].keys():
                if players.get('players')[player]:
                    playersInRaid += f'players.get(\'players\')[{player}][\'nickname\'],'
                continue
            newField = {
                'startedBy': data['headlessRequesterNickname'],
                'faction': ('SCAV' if data['side'] == 'Savage' else data['side']),
                'map': data['location'],
                'time': data['time'],
                'players': playersInRaid[:-1]
            }
        return newField
    
    @commands.command()
    async def test(self, ctx):
        channel = self.bot.get_channel(1312855728439955516)
        message = await channel.fetch_message(1357450159981854911)
        embed = message.embeds[0]
        print(embed.fields)
