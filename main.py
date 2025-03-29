import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

from cogs.tarkov import Tarkov

load_dotenv()

MY_GUILD = discord.Object(id=int(os.getenv('MY_GUILD')))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

cogsToLoad = ['error', 'help', 'nsfw', 'owner', 'reminder']

@bot.tree.command(name="hello", description="Says Hello!", guild=MY_GUILD)
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hello, {interaction.user.mention}!')

@bot.event
async def on_ready():
    #await bot.tree.sync(guild=MY_GUILD)
    await bot.add_cog(Tarkov(bot))
    print(f'Logged in as {bot.user}.')
    print(await bot.tree.fetch_commands(guild=MY_GUILD))




bot.run(os.getenv('BOT_TOKEN'))