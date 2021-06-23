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

#challonge
challonge.set_credentials(KEYS.challongeUser, KEYS.challongeAPI)


@client.group(aliases = ['t', 'tourney'])
async def tournament(ctx): 
    '''
    Get Tourney info
    '''
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid sub command passed...')

@tournament.command(aliases = ['addp'])
async def addParticipant(ctx, a :str = '', b :str = ''):
    response = 'empty'
    if a=='' or b == '':
        await ctx.send("Please enter participants name and id.\n eg: `h.t addp vinay 506018589904470047`")
    else:
        c = a + ' ' + b
        response = challonge.participants.create('a9mlgb9p', c)
        await ctx.send(response)
    

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    owner = client.get_user(506018589904470047)
    await owner.send("im up..! - ")


@client.command()
async def sendDM(ctx):
    remind = client.get_user(506018589904470047)

    await sendmessage(remind, 1)
    await sendmessage(remind, 2)
client.run(KEYS.discordToken)
