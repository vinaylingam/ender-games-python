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
client = commands.Bot(command_prefix = 'h..', 
                      case_insensitive=True,
                     intents=intents,
                     help_command=None)

@client.command()
async def s(ctx):
    embed = discord.Embed(color=0xbd513e)

    embed.set_footer(text='if you are wondering: yes, this is an event. See more info with "rpg help random events"')
    embed.add_field(name = ':gem: **OOPS! God accidentally dropped an EPIC coin**', 
                    value = 'The first player who types the following sentence will get it!\n**HEY EPIC NPC! I WANT TO TRADE WITH YOU**', 
                    inline = False)
    await ctx.send(embed=embed)


#--------- Events ----------#
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    owner = client.get_user(506018589904470047)
    await owner.send("im up..! - ")

client.run(KEYS.discordTestToken)