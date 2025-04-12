import os

from discord.ext import commands

from utils.logging_helpers import log_cog_add_failure, log_cog_add_success


async def load_cogs(bot: commands.Bot, cog_name="") -> None:
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            module_name = file[:-3]

            if cog_name and cog_name != module_name:
                continue

            try:
                await bot.load_extension(f"cogs.{module_name}")
                log_cog_add_success(module_name)
            except Exception as e:
                log_cog_add_failure(module_name, e)
