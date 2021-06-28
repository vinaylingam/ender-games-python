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


@client.command()
async def settings(ctx):
    dmenable = "True" if reminderStates['isDmSendEnabled'] else "False"
    await ctx.send("isDmSendEnabled: " + dmenable)

@client.command()
async def user_details(ctx, a:int = None):
    try: 
        user = client.get_user(a)
        await ctx.send(user.name)
    except:
        await ctx.send("invalid id")

@client.command()
async def help(ctx, a:str = None):
    embed = discord.Embed(color=0xFCDCF5)
    embed.set_author(name = 'ender games',
                     icon_url = 'https://cdn.discordapp.com/avatars/786278859775017061/e729d473a2c2536d3f0db8bbe36af627.png')
    if a is None:
        embed.title = "**ender games help**"
        embed.set_footer(text='Use "h.help command" for more info on a command.')
        embed.add_field(
            name = 'Miscelleanous',
            value = '`ping`, `rng`, `calculate`',
            inline = False,
        )
        await ctx.send(embed=embed)
    elif a == 'ping':
        embed.title = "**command: ping**"
        embed.description = "To see the latency in ms(milliseconds)."
        await ctx.send(embed=embed)
        pass
    elif a == 'rng':
        embed.title = "**command: rng**"
        embed.description = """A random number generator between two numbers. \n
                            Alias: None \u200b eg: h.rng [a] [b] [c=1(max:10)]\n
                            picks a random number c number of times between a and b.\n
                            a,b,c should be non negative and a <= b"""
        await ctx.send(embed=embed)
        pass
    elif a in ['calculate', 'calc', 'c']:
        embed.title = "**command: calculte**"
        embed.description = """A Basic calculatoar. uwu \n
                            Aliases: c, calc \n
                            eg: h.calc (1+2-3/4) \n
                            returns: a message, if expression is not valid.
                            """
        await ctx.send(embed=embed)
        pass
    else:
        await ctx.send("command not found..!")


#--------- Events ----------#
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    owner = client.get_user(506018589904470047)
    await owner.send("im up..! - ")


@client.event
async def on_message(message):
    if client.user.id == message.author.id:
        return

    if message.content.find('<@786278859775017061>') != -1:
        message.channel.send("My prefix here is `h.`")

    if message.channel.id == 858198717898162196:
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
client.run(KEYS.discordToken)
