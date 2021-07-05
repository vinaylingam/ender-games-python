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
client = commands.Bot(command_prefix = '.h.', 
                      case_insensitive=True,
                     intents=intents,
                     help_command=None)

#challonge.set_credentials(KEYS.challongeUser, KEYS.challongeAPI)

reminderStates = defaultdict(bool)

#--------- Miscelleanous functions ----------#
async def reminder(time, id, msgBeforeReminder, msgAfterReminder, which = '', where = 'Channel'):
    if where == 'Channel':
        remind = client.get_channel(id)
    else: # DM's
        remind = client.get_user(id)

    if which != '' and reminderStates[which] == True:
        await remind.send('reminder is already Set..!')
        return

    await remind.send(msgBeforeReminder)
    if which != '':
        reminderStates[which] = True
    await asyncio.sleep(time)
    await remind.send(msgAfterReminder)
    if which != '':
        reminderStates[which] = False
    
def printTime():
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    utc = datetime.now(timezone('UTC'))
    ist = utc.astimezone(timezone('Asia/Kolkata'))
    return ist.strftime(format)

#------- commands -------#
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
    print('We have logged in as {0.user}'.format(client))
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
            #await message.channel.send(embed.to_dict())
            print(embed.to_dict())

    channel = message.channel
    channelId = channel.id
    if channelId in [857682775578378270, 678167360837779466]:
        if message.author.id == 302050872383242240: # disboard ID
            msg1 = ''
            if len(message.embeds) > 0:
                embed = message.embeds[0]
                description = embed.description
                if description.find('Bump done') != -1:
                    minutes = 120
                    personBumped, temps = description.split(', \n')
                    msg1 = personBumped + ', Ty for bumping.\n'
                elif description.find('Please wait another') != -1:
                    temps0, temps1 = description.split(', Please wait another ')
                    temps2 = list(temps1.split())
                    minutes = int(temps2[0])

                time = minutes*60 # in seconds
                msg1 += 'i will remind you to bump in {}mins.'.format(minutes)
                msg2 = '<@506018589904470047>, you can bump the server again....!'
                await reminder(time, channelId, msg1, msg2, 'bumpRem') 

    await client.process_commands(message)
client.run('a')
