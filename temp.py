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

challonge
#challonge.set_credentials(KEYS.challongeUser, KEYS.challongeAPI)

reminderStates = defaultdict(bool)

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

def printTime():
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    utc = datetime.now(timezone('UTC'))
    ist = utc.astimezone(timezone('Asia/Kolkata'))
    return ist.strftime(format)

@client.command()
async def settings(ctx):
    dmenable = "True" if reminderStates['isDmSendEnabled'] else "False"
    await ctx.send("isDmSendEnabled: " + dmenable)

@client.command()
async def sendDM(ctx):
    remind = client.get_user(506018589904470047)
    await remind.send("testing " + printTime())
    await asyncio.create_task(sendmessage(remind, 60))
    await asyncio.create_task(sendmessage(remind, 90))

async def sendmessage(obj, time):
    if not reminderStates['isDmSendEnabled']:
        reminderStates['isDmSendEnabled'] = True
        await asyncio.sleep(time)
        await obj.send("testing asynchio-tasks. " + printTime())
        reminderStates['isDmSendEnabled'] = False
    else:
        await obj.send("Reminder is already set..!")



@client.event
async def on_message(message):
    if client.user.id == message.author.id:
        return

    if message.author.id == 302050872383242240: # disboard
        await message.channel.send(str(message.channel.id) + ' ' + str(message.id) + ' ' + str(message.author.name) + ' ' + str(message.content))
        await message.channel.send(message)
        with open("logs.txt", "a+", encoding="utf-8") as f:
            await message.channel.send(message)
        embeds = message.embeds
        print(len(embeds))
        for embed in embeds:
            print(embed.to_dict())
            with open("logs.txt", "a+", encoding="utf-8") as f:
                await message.channel.send(embed.to_dict())
        print()

client.run(KEYS.discordToken)
