import discord
from dotenv import load_dotenv
import os

load_dotenv()

class MyClient(discord.client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        if message.author == client.user:
            return
        
        if message.content.startswith('!hello'):
            print(f'Message from {message.author}: {message.content}')
            await message.channel.send('hello!')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('BOT_TOKEN'))