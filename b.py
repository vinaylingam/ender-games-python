import discord
from discord.ext import commands
import random
import KEYS
import logging
#import pyrebase
import json
import asyncio
import threading 
from datetime import datetime
from pytz import timezone
from collections import defaultdict
import challonge

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename = "logs.txt")


intents = discord.Intents.default()  # All but the two privileged ones
intents.members = True  # Subscribe to the Members intent
client = commands.Bot(command_prefix = 'h.', case_insensitive=True, intents=intents)

@client.command()
async def  tinfo(ctx):


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    owner = client.get_user(506018589904470047)
    await owner.send("im up..! - ")


client.run(KEYS.discordToken)
