import asyncio
import os

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from cogs.customEmbed import customEmbed
from methods import fileHandling, loadPlayers
from methods.cogLoading import load_cogs
from utils.logging_helpers import log_cog_load_failure, log_cog_load_success, logger, setup_command_hooks

load_dotenv()

MY_GUILD = discord.Object(id=int(os.getenv("MY_GUILD")))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

setup_command_hooks(bot)


@bot.tree.command(name="hello", description="Says Hello!", guild=MY_GUILD)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!")


async def updateTarkovEmbeds() -> None:
    bot.wait_until_ready()


@bot.event
async def on_ready():
    # await bot.tree.sync(guild=MY_GUILD)
    await load_cogs(bot)
    newPLayers = loadPlayers.build_playerlist()
    fileHandling.saveJson(f"{os.getcwd()}/.private_stuff/players.json", newPLayers)

    print(f"Logged in as {bot.user}.")
    print(await bot.tree.fetch_commands(guild=MY_GUILD))

    while not bot.is_closed():
        embeds = customEmbed(bot)
        await embeds.edit_embed("headless")
        await embeds.edit_embed("players")
        logger.info("Embeds updated!")
        await asyncio.sleep(60)


bot.run(os.getenv("BOT_TOKEN"))
