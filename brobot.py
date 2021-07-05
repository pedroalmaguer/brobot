#hello

# bot.py
import os
import logging
import discord
from dotenv import load_dotenv

load_dotenv('/env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# logging shiz
# https://discordpy.readthedocs.io/en/stable/logging.html
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(Levelname)s: %(message)s'))
logger.addHandler(handler)


client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
@client.event
async def on_message(message):

    # bot ignores messages fromt self
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello')
        return

        
client.run(TOKEN)