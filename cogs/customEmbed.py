import os
from datetime import datetime, timezone

from discord import Embed
from discord.ext import commands
from dotenv import load_dotenv

from methods import apiRequests, fileHandling

load_dotenv()


class embedBuilder:
    def __init__(self, bot, current_dir, map_list):
        self.bot = bot
        self.current_dir = current_dir
        self.map_list = map_list

    async def load_embed(self, ctx, name: str) -> Embed:
        data = fileHandling.loadJson(f"{self.current_dir}/lists/embeds.json")
        embed_list: dict = data.get(name)
        channel = self.bot.get_channel(int(embed_list["channelID"]))
        message = await channel.fetch_message(int(embed_list["messageID"]))
        embed = message.embeds[0]
        return embed.copy()

    async def generate_embed(self, ctx, name: str) -> None:
        """Creates embed in default structure and saves it to json under identifier with message id and channel id

        Args:
            ctx (_type_): message
            name (str): Identifier used to save info into json
        """
        pass

    async def edit_embed(self, ctx, name: str) -> None:
        """Modifies embed saved in json under specified identifier.

        Args:
            ctx (_type_): message
            name (str): Identifier used to load info from json
        """
        pass

    async def build_embed(self, data: dict, mode="") -> str:
        """Constructs parts of embed so it can be used to either build or edit embed.

        Args:
            data (dict): Data with which will be the part of embed build
            mode (str): which component of the embed should be edited. WIP

        Returns:
            str: returns string that contains everything needed to build the component.
        """
        players = fileHandling.loadJson(f"{self.current_dir}/.private_stuff/players.json")
        playersInRaid = ""
        for player in data["players"].keys():
            if player in players.get("players").keys():
                playersInRaid += players.get("players")[player]["nickname"] + ", "
                continue
        newField = f"Started By: {data['headlessRequesterNickname']}\nFaction: {('SCAV' if data['side'] == 'Savage' else data['side'])}\nMap: {self.map_list.get(data['location'])}\nTime: {data['time']}\nPlayers: {playersInRaid[:-2]}"
        return newField


class headlessEmbed(embedBuilder):
    def __init__(self, bot, current_dir, map_list):
        self.bot = bot
        self.current_dir = current_dir
        self.map_list = map_list
        self.server_ip = os.getenv("SERVER_IP")

    async def generate_embed(self, ctx, name):
        data = fileHandling.loadJson(f"{self.current_dir}/lists/embeds.json")

        embed = Embed(title="Headless Servers", colour=0x00B0F4, timestamp=datetime.now())

        embed.add_field(
            name="{Headless Name}",
            value="Started By: {playerName}\nSide?: {side}\nMap: {raidMap}\nPlayers: {playerList}",
            inline=True,
        )
        embed.add_field(
            name="{Headless Name}",
            value="Started By: {playerName}\nSide?: {side}\nMap: {raidMap}\nPlayers: {playerList}",
            inline=True,
        )
        embed.set_footer(text="Obskurion", icon_url="https://files.mkomanek.eu/-d4QrYaTTGy/profilePicture.png")

        data[name] = {"messageID": ctx.message.id, "channelID": ctx.channel.id}

        fileHandling.saveJson(f"{self.current_dir}/lists/embeds.json", data)
        await ctx.send(embed=embed)

    async def edit_embed(self, ctx, name):
        data = fileHandling.loadJson(f"{self.current_dir}/lists/embeds.json")
        embed_list: dict = data.get(name)
        channel = self.bot.get_channel(int(embed_list["channelID"]))
        message = await channel.fetch_message(int(embed_list["messageID"]))
        embed = message.embeds[0]

        path = "fika/location/raids"
        serverID_Delta = "67e67855afdbd623a800223c"
        serverID_Gamma = "67e67855afdbd623a8002379"

        data = apiRequests.request_data(apiRequests.build_url(self.server_ip, 6969, path))

        embed = embed.copy()

        field_1 = "Server is Idle"
        field_2 = "Server is Idle"

        for raid in data:
            if raid["serverId"] == serverID_Delta:
                field_1 = await self.build_embed(raid, name)
            elif raid["serverId"] == serverID_Gamma:
                field_2 = await self.build_embed(raid, name)

        embed.set_field_at(index=0, name="Delta", value=field_1, inline=True)
        embed.set_field_at(index=1, name="Gamma", value=field_2, inline=True)

        embed.timestamp = datetime.now(timezone.utc)

        await message.edit(embed=embed)

    async def build_embed(self, data, mode=""):
        return await super().build_embed(data, mode)


class playerEmbed(embedBuilder):
    def __init__(self, bot, current_dir, map_list):
        self.bot = bot
        self.current_dir = current_dir
        self.map_list = map_list
        self.server_ip = os.getenv("SERVER_IP")

    async def generate_embed(self, ctx, name):
        data = fileHandling.loadJson(f"{self.current_dir}/lists/embeds.json")

        embed = Embed(title="Player Raids", colour=0x00B0F4, timestamp=datetime.now())

        embed.add_field(
            name="{Player Name}",
            value="Side?: {side}\nMap: {raidMap}\nPlayers: {playerList}",
            inline=True,
        )
        embed.add_field(
            name="{Player Name}",
            value="Side?: {side}\nMap: {raidMap}\nPlayers: {playerList}",
            inline=True,
        )
        embed.set_footer(text="Obskurion", icon_url="https://files.mkomanek.eu/-d4QrYaTTGy/profilePicture.png")

        data[name] = {"messageID": ctx.message.id, "channelID": ctx.channel.id}

        fileHandling.saveJson(f"{self.current_dir}/lists/embeds.json", data)
        await ctx.send(embed=embed)

    async def build_embed(self, data, mode=""):
        return await super().build_embed(data, mode)

    async def edit_embed(self, ctx, name):
        # Load embed from json by the identifier
        data = fileHandling.loadJson(f"{self.current_dir}/lists/embeds.json")
        embed_list: dict = data.get(name)
        channel = self.bot.get_channel(int(embed_list["channelID"]))
        message = await channel.fetch_message(int(embed_list["messageID"]))
        embed: Embed = message.embeds[0]

        # Define API path and Headless server UUIDs # TODO load the UUIDs from json (in case there will be more than two headlesses)
        path = "fika/location/raids"
        serverID_Delta = "67e67855afdbd623a800223c"
        serverID_Gamma = "67e67855afdbd623a8002379"

        data = apiRequests.request_data(apiRequests.build_url(self.server_ip, 6969, path))

        default_field = "There are no active player raids"

        embed = embed.copy()

        # Reset all fields
        embed.clear_fields()

        if len(data) > 0:
            for raid in data:
                if raid["serverId"] == serverID_Delta or raid["serverId"] == serverID_Gamma:
                    continue
                embed.add_field(name=f"{raid['headlessRequesterNickname']}", value=await self.build_embed(raid, name), inline=True)
        else:
            embed.add_field(name="Offline", value=default_field, inline=True)

        embed.timestamp = datetime.now(timezone.utc)

        await message.edit(embed=embed)


class customEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_dir = os.getcwd()
        self.map_list = {
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
            "sandbox_high": "Ground Zero (21+)",
        }

    @commands.command()
    async def generate_embed(self, ctx, name: str) -> None:
        """_summary_

        Args:
            ctx (_type_): _description_
            name (str): _description_
        """
        if name == "headless":
            embedBuilder = headlessEmbed(self.bot, self.current_dir, self.map_list)
        elif name == "players":
            embedBuilder = playerEmbed(self.bot, self.current_dir, self.map_list)
        if "embedBuilder" in locals() or "embedBuilder" in globals():
            await embedBuilder.generate_embed(ctx, name)

    @commands.command()
    async def edit_embed(self, ctx, name: str) -> None:
        """_summary_

        Args:
            ctx (_type_): _description_
            name (str): _description_
        """
        if name == "headless":
            embed = headlessEmbed(self.bot, self.current_dir, self.map_list)
        elif name == "players":
            embed = playerEmbed(self.bot, self.current_dir, self.map_list)

        await embed.edit_embed(ctx, name)


async def setup(bot: commands.Bot):
    await bot.add_cog(customEmbed(bot))
