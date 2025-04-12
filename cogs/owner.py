from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()


class Owner(commands.Cog):
    """_summary_

    Args:
        commands (_type_): _description_
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx):
        channel = self.bot.get_channel(1312855728439955516)
        message = await channel.fetch_message(1357450159981854911)
        embed = message.embeds[0]
        print(embed.fields)
