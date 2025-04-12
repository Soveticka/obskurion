import importlib
import os

from discord.ext import commands


async def load_cogs(bot: commands.Bot) -> None:
    for file in os.listdir("./cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            module_name = file[:-3]
            module_path = f"cogs.{module_name}"

            try:
                module = importlib.import_module(module_path)
                cog_class = getattr(module, module_name)
                await bot.add_cog(cog_class(bot))
                print(f"Loaded cog: {module_name}")
            except Exception as e:
                print(f"Failed to load cog: {module_name}. Error: {e}")
