import discord
from discord.ext import commands
import random
import KEYS
import logging
import pyrebase

#logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger('discord')
#logger.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
#handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
#logger.addHandler(handler)

config = {
  "apiKey": KEYS.apiKey,
  "authDomain": KEYS.authDomain,
  "databaseURL": KEYS.databaseURL,
  "storageBucket": KEYS.storageBucket,
  "serviceAccount": KEYS.pathToServiceJson
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

data = {"serverid" :2, "channelid" : 4}
db.child('servers').child(1).set(data)

client = commands.Bot(command_prefix = 'h.')


#---------Commands----------#
@client.command()
async def ping(ctx):
    """
    To see the latency in ms(milliseconds).
    """
    print(ctx)
    await ctx.send(f'pong! {round(client.latency * 1000)}ms')

@client.command()
async def rng(ctx,*, args):
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

@client.command()
async def arena(ctx, *, args):
    """
    let's you join a group arena
    """


#--------events-----------#
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    print(message.id, message.author.name, message.content)
    print(message)
    embeds = message.embeds
    for embed in embeds:
        print(embed.to_dict())
    print()
    #s = list(message.content.split())
    #ss = []
    #for i in s:
    #    ss.append(i.lower())
    #if 'need' in ss:
    #    await message.channel.send('don\'t we all?')
    await client.process_commands(message)

client.run(KEYS.token)
