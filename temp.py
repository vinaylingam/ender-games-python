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
client = commands.Bot(command_prefix = 'h.', 
                      case_insensitive=True,
                     intents=intents,
                     help_command=None)

#challonge.set_credentials(KEYS.challongeUser, KEYS.challongeAPI)
    
def printTime():
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    utc = datetime.now(timezone('UTC'))
    ist = utc.astimezone(timezone('Asia/Kolkata'))
    return ist.strftime(format)

#------- commands -------#
@client.command(aliases=['mdwi'])
async def messageDetailWithId(ctx, ch:discord.TextChannel, id:int = None):

    message = await ch.fetch_message(id)
        
    await ctx.send(str(message.channel.id) + ' ' + str(message.id) + ' ' + str(message.author.name) + ' ' + str(message.content))
    await ctx.send( message)
    embeds = message.embeds
    for embed in embeds:
        await ctx.send(embed.to_dict())
        print(embed.to_dict())


#@client.group(aliases = ['t', 'tourney'])
#async def tournament(ctx): 
#    '''
#    Get Tourney info
#    '''
#    if ctx.invoked_subcommand is None:
#        await ctx.send('Invalid sub command passed...')

#@tournament.command(aliases = ['addp'])
#async def addParticipant(ctx, a :str = '', b :str = ''):
#    response = 'empty'
#    if a=='' or b == '':
#        await ctx.send("Please enter participants name and id.\n eg: `h.t addp vinay 506018589904470047`")
#    else:
#        c = a + ' ' + b
#        response = challonge.participants.create('a9mlgb9p', c)
#        await ctx.send(response)


#--------- Events ----------#
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    owner = client.get_user(506018589904470047)
    await owner.send("im up..! - ")


@client.event
async def on_message(message):
    if client.user.id == message.author.id or message.author.id == 786278859775017061:
        return

    if message.content.find('<@!860015378816958464>') != -1:
        await message.channel.send("My prefix here is `.h.`")

    if message.channel.id == 860017662671061012:
        await message.channel.send(str(message.channel.id) + ' ' + str(message.id) + ' ' + str(message.author.name) + ' ' + str(message.content))
        await message.channel.send( message)
        embeds = message.embeds
        for embed in embeds:
            await message.channel.send(embed.to_dict())
            print(embed.to_dict())

    # Special Trades / Random event drops
    if message.author.id == 860015378816958464:#555955826880413696:
        if len(message.embeds) > 0:
            embed = message.embeds[0]
            if len(embed.fields) >0:
                fields = embed.fields[0]
                if fields.value.find('The first player who types the following sentence will get it!') != -1:
                    playerMsg, rewardMsg = fields.value.split('\n')
                    await message.channel.send(rewardMsg)


    await client.process_commands(message)
client.run(KEYS.discordToken)
