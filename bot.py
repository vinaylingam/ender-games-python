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
client = commands.Bot(command_prefix = 'h.',
                     case_insensitive=True,
                    intents=intents,
                    help_command = None)

reminders = defaultdict(int)
reminderStates = defaultdict(bool)

#---------Commands----------#
@client.command()
async def ping(ctx, case_insensitive=True):
    """
    To see the latency in ms(milliseconds).
    """
    print(ctx)
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

@client.command()
async def rng(ctx,*, args='', case_insensitive=True):
    """
    A random number generator between two numbers.
    Alias: None
    eg: h.rng [a] [b] [c=1(max:10)]
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
                await ctx.send('i can only pick at most 10 numbers.')
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
async def calculate(ctx,*,args = None):
    """
    A Basic calculatoar. uwu
    Aliases: c, calc
    eg: h.calc (1+2-3/4)
    returns: a message, if expression is not valid.
    """
    if args is None:
        await ctx.send("please, enter proper expresision....!")
        return

    expr = list(args.split())
    expr = ''.join(expr)
    expp = expr.replace('x','*')

    ans = ''
    try:
        ans = round(eval(expp),2)
        await ctx.send(ans)
    except:
        await ctx.send("that's not a valid expression!")  
        return

@client.command()
async def help(ctx, a:str = None, case_insensitive=True):
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
    elif a == 'rng':
        embed.title = "**command: rng**"
        description = "A random number generator between two numbers. \n"
        description += "**Alias:** None \n"
        description += "**eg:** `h.rng [a] [b] [c=1(max:10)]`\n"
        description += "**description:** picks a random number c number of times between a and b.\n"
        description += "**Notes:** a,b,c should be non negative and a <= b"
        embed.description = description
        await ctx.send(embed=embed)
    elif a in ['calculate', 'calc', 'c']:
        embed.title = "**command: calculte**"
        description = "A Basic calculatoar. uwu \n"
        description += "**Alias:** c, calc \n"
        description += "**eg:** h.calc (1+2-3/4) \n"
        description += "**description:** returns an calculated expression/ a message, if expression is not valid."
        embed.description = description                    
        await ctx.send(embed=embed)
    else:
        await ctx.send("command not found..!")

@client.command(aliases = ['mir'])
async def membersinrole(ctx, idn:str = None, case_insensitive=True):
    """
    Gives Name and id of the ppl who has the role.
    Alias: mir
    **eg:** h.mir <id/Name>
    """
    if idn is None:
        await ctx.send("Please enter role id / name")
        return

    def retRole(rr, ri, rn):
        rrole = None
        if ri is None:
            for i in rr:
                if i.name.lower() == rn.lower():
                    rrole = i
                    break
        else:
            for i in rr:
                if int(i.id) == int(ri):
                    rrole = i 
                    break
        return rrole

    roles = ctx.guild.roles
    roleid = None
    rolename = None
    if idn.isnumeric():
        roleid = idn
    else:
        rolename = idn
    
    role = retRole(roles, roleid, rolename)
    if role is None:
        await ctx.send("that role id / name is not found in server.")
        return

    members = role.members

    if len(members) == 0:
        await ctx.send('There are no members in this role.')

    embed = discord.Embed(color=0xFCDCF5)
    embed.type = 'rich'
    embed.set_author(name = 'ender games',
                     icon_url = 'https://cdn.discordapp.com/avatars/786278859775017061/e729d473a2c2536d3f0db8bbe36af627.png')
    embed.title = f'Role: {role.name} ({role.id})\n\n'
    embed.set_footer(text=f'Page no. related info will be filled')
    description = f'**Members:**\n\n'
    
    for c,m in enumerate(members,1):
        description += f'**#{c} | {m.name}** ({m.id})\n\n'
    embed.description = description
    await ctx.send(embed=embed)

@client.command(aliases=['mdwi'])
async def messageDetailWithId(ctx, ch:discord.TextChannel, id:int = None, case_insensitive=True):

    message = await ch.fetch_message(id)
        
    await ctx.send(str(message.channel.id) + ' ' + str(message.id) + ' ' + str(message.author.name) + ' ' + str(message.content))
    await ctx.send( message)
    embeds = message.embeds
    for embed in embeds:
        await ctx.send(embed.to_dict())
        print(embed.to_dict())

# miscelleanous functions
async def reminder(time, id, msgBeforeReminder = None, msgAfterReminder = None, which = None, where = 'Channel'):
    if where == 'Channel':
        remind = client.get_channel(id)
    else: # DM's
        remind = client.get_user(id)

    if which != '' and reminderStates[which] == True:
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

#--------events-----------#
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    owner = client.get_user(506018589904470047)
    await owner.send("im up..! - "+ printTime())

@client.event
async def on_message(message):

    owner = client.get_user(506018589904470047)
    if client.user.id == message.author.id:
        return

    if message.content.find('<@!786278859775017061>') != -1 or message.content.find('<@786278859775017061>') != -1:
        message.channel.send("My prefix here is `h.`")

    if message.channel.id == 858198717898162196:
        await message.channel.send(str(message.channel.id) + ' ' + str(message.id) + ' ' + str(message.author.name) + ' ' + str(message.content))
        await message.channel.send( message)
        embeds = message.embeds
        for embed in embeds:
            await message.channel.send(embed.to_dict())

    channel = message.channel
    channelId = channel.id 

    # guild raid/upgrade reminder
    if channelId in [770453997433126933,740918396685910096, 780164101376442368, 778167058537775112]:
        if message.author.id == 555955826880413696: # Epic RPG Bot ID
            if len(message.embeds) >0:
                embed = message.embeds[0]
                title, description = embed.title, embed.description
                title = title.lower() if len(embed.title) != 0 else ''
                description = description.lower() if len(description) != 0 else ''
                if title.find('guild') != -1 or description.find('raided') != -1 or description.find('upgrade') != -1 :
                    if title.find("your guild has already raided or been upgraded, wait at least **") != -1:
                        text, h = title.split("wait at least **")
                        hour, m = h.split("h ")
                        min, s = m.split("m ")
                        sec, temp = s.split("s")
                        reminders['h'], reminders['m'], reminders['s'] = int(hour), int(min), int(sec)
                    else:
                        reminders['h'], reminders['m'], reminders['s'] = 2, 0, 0
                
                    time = (reminders['h']*60 + reminders['m'])*60 + reminders['s'] # in seconds
                    msg1 = f"reminder is set for {reminders['h']}h {reminders['m']}m {reminders['s']}seconds....! <:teehee:775029757690773517>"
                    msg2 = '<@506018589904470047>, rpg guild raid/upgrade is ready....!'

                    await reminder(time, channelId, msg1, msg2, 'guildRem') 
    
    # disboard reminder                                                       
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

                await message.channel.send(msg1)
                #time = minutes*60 # in seconds
                #msg2 = '<@506018589904470047>, you can bump the server again....!'
                #await reminder(time,channelId,msg1, msg2, which = 'bump'+str(channelId))
    
    # Special Trades / Random event drops
    if message.author.id == 555955826880413696: # Epic RPG Bot ID
        if len(message.embeds) > 0:
            embed = message.embeds[0]
            if len(embed.fields) >0:
                fields = embed.fields[0]
                if fields.value.find('The first player who types the following sentence will get it!') != -1:
                    playerMsg, rewardMsg = fields.value.split('\n')
                    await message.channel.send(rewardMsg)
                    await owner.send(f"[special trade](https://discord.com/{message.guild.id}/{message.channel.id}/{message.id}) - Triggered by: {message.author.name} in <#{message.channel.id}>")

    # with open("logs.txt", "a+", encoding="utf-8") as f:
    #     print(message, sep='\n\n', file=f)
    # embeds = message.embeds
    # for embed in embeds:
    #     print(embed.to_dict())
    #     with open("logs.txt", "a+", encoding="utf-8") as f:
    #         print(embed.to_dict(), sep='\n\n', file=f)
    
    await client.process_commands(message)

client.run(KEYS.discordToken)
