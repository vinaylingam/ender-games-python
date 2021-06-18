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

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename = "logs.txt")

#config = {
#  "apiKey": KEYS.apiKeyFirebase,
#  "authDomain": KEYS.authDomain,
#  "databaseURL": KEYS.databaseURL,
#  "storageBucket": KEYS.storageBucket,
#  "serviceAccount": KEYS.pathToServiceJson
#}

#firebase = pyrebase.initialize_app(config)
#db = firebase.database()

intents = discord.Intents.default()  # All but the two privileged ones
intents.members = True  # Subscribe to the Members intent
client = commands.Bot(command_prefix = 'h.', case_insensitive=True, intents=intents)

reminders = defaultdict(int)

#---------Commands----------#
@client.command()
async def ping(ctx):
    """
    To see the latency in ms(milliseconds).
    """
    print(ctx)
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

@client.command()
async def rng(ctx,*, args=''):
    """
    h.rng [a] [b] [c=1(max:10)]
    picks a random number c number of times between a and b.
    a,b,c should be non negative and a <= b
    """
    try:
        warn = ''
        arr = list(map(int,args.split()))
        if len(arr) == 1:
            warn = 'Need atleast 2 more numbers for me to work....!'
            await ctx.send(warn)
            return
        elif len(arr) == 2:
            c=1
            a, b = arr[0], arr[1]
        else:
            a, b, c = arr[0], arr[1], arr[2]
            if c>10:
                await ctx.send('10 is the limit of number')
                c = 10
            if c>(b-a+1):
                c = b-a+1

        if a<0 or b<0 or c<0:
            warn += 'Bruhh!! numbers should be >0'
        if a>b:
            if len(warn) != 0:
                warn += ', '
            warn += ':neutral_face: First number should be greater than 2nd'
        if len(warn) == 0:
            seq = [i for i in range(a,b+1)]
            nums = random.sample(seq, k=c)
            print(nums)
            numsS = ''
            for i in nums:
                numsS += str(i) + ' '
            await ctx.send(numsS)
        else:
            await ctx.send(warn)
    except:
        await ctx.send('hmm check `h.help rng`')

@client.command(aliases=['c','calc'], case_insensitive=True)
async def calculate(ctx,*,args=''):
    if args == '':
        await ctx.send("please, enter proper expresision....!")
        return

    expr = list(args.split())
    expr = ''.join(expr)
    expp = expr.replace('x','*')

    ans = ''
    try:
        print(expr)
        ans = eval(expp)
        await ctx.send(ans)
    except:
        await ctx.send("that's not a valid expression!")  
        return

@client.command()
async def history(ctx, limit: int = 100): 
    if ctx.author.id != 506018589904470047:
        await ctx.send("You don't have perms to do this command. now scramm.. shuu.. shuu...")
        return
    try:
        messages = await ctx.channel.history(limit=limit).flatten()
        with open("guild.txt", "a+", encoding="utf-8") as f:
            for message in messages:
                print(message, sep='\n\n', file=f)
                embeds = message.embeds
                for e in embeds:
                    print(e, sep="\n\n", file=f)
        await ctx.send("Succesfully written.")
    except:
        await ctx.send("Error occured")

#@client.command()
#async def whois(ctx, *, args=''):
#    """
#    Gives the info about User.
#    """
#    #try:
#    id = args.strip()
#    fuser = await client.fetch_user(id)
#    logging.info(fuser)
#    await ctx.send('got it.')
#    #except:
#    #    warn = 'hmm..! i need a id to help you.'
#    #    await ctx.send(warn)

#@client.command()
#async def clan(ctx, *, args = ''):
#    if args == '':
#        await ctx.send('hmm..')
#        return
#    inputs = list(args.split())

#    authorID = int(f'{ctx.author.id}')
#    serverID = int(f'{ctx.author.guild.id}')
#    adminn = db.child("Admins").child(serverID).get()
#    print(adminn.val())
#    admins = []
#    for i in adminn.each():
#        admins.append(int(i.val()))
#    if inputs[0] == "add":
#        if len(inputs) == 1:
#            await ctx.send("smh... give me a id...")
#            return
#        if authorID in admins:
#            try:
#                userToAdd = int(inputs[1])
#            except:
#                await ctx.send("smh... give me a id...")
#            #  VERIFY THE USER
#            #db.child("clanMembers").child(serverID).push(userToAdd)
#            await ctx.send('admin checked')
#        else:
#            await ctx.send("You are not authorised to use this command...!")
#    return


# miscelleanous functions
async def reminder(time, id, msg, where = 'Channel'):
    await asyncio.sleep(time)
    if where == 'Channel':
        remind = client.get_channel(id)
    else: # DM's
        remind = client.get_user(id)
    await remind.send(msg)

def printTime():
    format = "%Y-%m-%d %H:%M:%S %Z%z"
    utc = datetime.now(timezone('UTC'))
    ist = utc.astimezone(timezone('Asia/Kolkata'))
    return ist.strftime(format)

#--------events-----------#
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    owner = client.get_user(506018589904470047)
    await owner.send("im up..! - "+ printTime() )

@client.event
async def on_message(message):

    if client.user.id == message.author.id:
        return

    # guild raid/upgrade reminders
    channel = message.channel
    channelId = channel.id 
    if channelId in [770453997433126933,740918396685910096, 780164101376442368, 778167058537775112]:
        if message.author.id == 555955826880413696: # Epic RPG Bot ID
            if len(message.embeds) >0:
                embed = message.embeds[0]
                title = embed.title
                title = title.lower() if len(title) != 0 else False
                if title and (title.find('guild') != -1 or title.find('raided') != -1 or title.find('upgrade') != -1) :
                    if title.find("Your guild has already raided or been upgraded, wait at least **") != -1:
                        text, h = title.split("wait at least **")
                        hour, m = h.split("h ")
                        reminders["h"]=int(hour)
                        min, s = m.split("m ")
                        reminders["m"]=int(min)
                        sec, temp = s.split("s")
                        reminders["s"]=int(sec)
                    else:
                        reminders['h']=2
                
                    await channel.send("reminder is set for {}h {}m {}seconds....! <:teehee:775029757690773517>".format(reminders["h"],reminders["m"],reminders["s"]))
                    time = (reminders['h']*60 + reminders['m'])*60 + reminders['s']
                    msg = '<@506018589904470047>, rpg guild raid/upgrade is ready....!'

                    logging.info(str(message.author.id) + 'triggered the guild command')
                    await reminder(time, channelId, msg)
                    await reminder(time-reminders['s'], 506018589904470047, msg)
        
    # logging.info("---"*50)
    # print(message.channel.id, message.id, message.author.name, message.content)
    # logging.info(str(message.channel.id) + ' ' + str(message.id) + ' ' + str(message.author.name) + ' ' + str(message.content))
    # print(message)
    # with open('logs.txt','a') as f:
    #     f.write(str(message))
    #     f.write('\n')
    # embeds = message.embeds
    # print(len(embeds))
    # for embed in embeds:
    #     print(embed.to_dict())
    #     with open('logs.txt','a') as f:
    #         f.write(str(embed.to_dict()))
    #         f.write('\n')
    #  print()
    
    await client.process_commands(message)

client.run(KEYS.discordToken)
