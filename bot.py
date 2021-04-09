import discord
from discord.ext import commands
import random
import KEYS
import logging
#import pyrebase
import json
import asyncio
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

client = commands.Bot(command_prefix = 'h.', case_insensitive=True)

reminders = defaultdict()

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

#--------events-----------#
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if client.user.id == message.author.id:
        return

    #def check(message):
    #    if message.author.id == 555955826880413696:
    #        embed = message.embeds[0]
    #        if embed.description == "Guild succesfully upgraded!" or embed.description.find("RAIDED") != 0:
    #            reminders['h']=2
    #        else:
    #            title = embed.title
    #            if title.find("wait at least **") != -1:
    #                text, h = title.split("wait at least **")
    #                h, m = h.split("h ")
    #                reminders["h"]=int(h)
    #                m, s = m.split("m ")
    #                reminders["m"]=int(m)
    #                s, temp = m.split("s")
    #                reminders["s"]=int(s)
    #        return True

    # guild raid/upgrade reminders
    #channel = message.channel
    #channelId = channel.id 
    #if channelId in [770453997433126933,740918396685910096, 780164101376442368]:
    #    contents = message.content.lower()
    #    if contents.find("rpg guild upgrade") == 0 or contents.find("rpg guild raid") == 0:
    #        try:
    #            await client.wait_for("message", timeout=3, check = check) 
    #            time = (reminders["h"]*60 + reminders["m"])*60 + reminders["s"]
    #            await channel.send("remainder is set for {}h {}m {}seconds....! <:teehee:775029757690773517>".format(reminders["h"],reminders["m"],reminders["s"]))
    #            await channel.send(time)
    #        except asyncio.TimeoutError:
    #            if channelId == 770453997433126933:
    #                await channel.send('<@&797418904162926642>, rpg guild raid/upgrade is ready....!')
    #            else:
    #                await channel.send('<@506018589904470047>, rpg guild raid/upgrade is ready....!')

    print(message.id, message.author.name, message.content)
    print(message)
    embeds = message.embeds
    print(len(embeds))
    for embed in embeds:
        print(embed.to_dict())
    print()
    await client.process_commands(message)

client.run(KEYS.discordToken)
