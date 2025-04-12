from discord.ext import commands
from dotenv import load_dotenv

from methods.cogLoading import load_cogs

load_dotenv()


class Owner(commands.Cog):
    """_summary_

    Args:
        commands (_type_): _description_
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def reload_cog(self, ctx, cog_name: str):
        try:
            await self.bot.reload_extension(f"cogs.{cog_name}")
            await ctx.reply(f"✅ Reloaded `{cog_name}` successfully.")
        except Exception as e:
            await ctx.reply(f"❌ Failed to reload `{cog_name}`: {e}")

    @commands.command()
    async def test(self, ctx):
        await ctx.reply("Worked!")


async def setup(bot: commands.Bot):
    await bot.add_cog(Owner(bot))
