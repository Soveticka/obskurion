from discord.ext import commands
from discord import Embed
from datetime import datetime
from methods import fileHandling
import os

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def generateEmbed(self, ctx, name: str) -> None:
        current_dir = os.getcwd()
        data = fileHandling.loadJson(f'{current_dir}/lists/embeds.json')

        embed = Embed(
            title="Headless Servers",
            colour=0x00b0f4,
            timestamp=datetime.now()
        )

        embed.add_field(name="{Headless Name}",
                value="Started By: {playerName}\nSide?: {side}\nMap:  {raidMap}\nPlayers: {playerList}",
                inline=True)
        embed.add_field(name="{Headless Name}",
                value="Started By: {playerName}\nSide?: {side}\nMap:  {raidMap}\nPlayers: {playerList}",
                inline=True)
        embed.set_footer(text="Obskurion",
                 icon_url="https://slate.dan.onl/slate.png")
        
        data[name] = {
            "messageID": ctx.message.id,
            "channelID": ctx.channel.id
        }

        fileHandling.saveJson(f'{current_dir}/lists/embeds.json', data)
        await ctx.send(embed=embed)
