import discord
from discord.ext import commands
import random
#import pyrebase
import asyncio 
from collections import defaultdict
import requests

class Miscellaneous(commands.Cog):
    """
    Some miscellaneous commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.reminders = defaultdict(int)
        self.reminderStates = defaultdict(bool)

    async def reminder(self, time, id, msgBeforeReminder = None, msgAfterReminder = None, which = None, where = 'Channel'):
        if where == 'Channel':
            remind = self.bot.get_channel(id)
        else: # DM's
            remind = self.bot.get_user(id)

        if which != '' and self.reminderStates[which] == True:
            return

        await remind.send(msgBeforeReminder)
        if which != '':
            self.reminderStates[which] = True
        await asyncio.sleep(time)
        await remind.send(msgAfterReminder)
        if which != '':
            self.reminderStates[which] = False

    @commands.command()
    async def ping(self, ctx, case_insensitive=True):
        """
        To see the latency in ms(milliseconds).
        """
        await ctx.send(f'pong! {round(self.bot.latency * 1000)}ms')
        
    @commands.command()
    async def rng(self, ctx, start:int = None, end:int = None, count:int = 1, case_insensitive=True):
        """
        A random number generator.
        **Usage**
        `h.rng <start> <end> <count>`
        **Alias** 
        None
        **description**
        picks a random number c number of times between a and b.
        a,b,c should be non negative and a <= b
        """        
        a, b, c = start, end, count
        try:
            warn = ''
            if a is None or b is None:
                warn = 'Need atleast 2 more numbers for me to work....!'
                await ctx.send(warn)
                return
            
            if c>10:
                await ctx.send('i can only pick at most 10 numbers.')
            c = min(min(10,c), b-a+1)

            if a<0 or b<0 or c<0:
                warn += 'Bruhh!! numbers should be >0'
            if a>b:
                if len(warn) != 0:
                    warn += ', '
                warn += ':neutral_face: First number should be greater than 2nd'
            if len(warn) == 0:
                seq = [i for i in range(a,b+1)]
                nums = random.sample(seq, k=c)
                numsS = ''
                for i in nums:
                    numsS += str(i) + ' '
                await ctx.send(numsS)
            else:
                await ctx.send(warn)
        except:
            await ctx.send('hmm check `h.help rng`')

    @commands.command(aliases=['c','calc'], case_insensitive=True)
    async def calculate(self, ctx,*,args = None):
        """
        A Basic calculatoar.
        **usage**
        `h.c ((1+2)*3-4)/5`
        **Aliases**
        c, calc
        **description**
        evaluates the given expression.
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

    @commands.Cog.listener()
    async def on_message(self, message):

        owner = self.bot.get_user(506018589904470047)
        if self.bot.user.id == message.author.id:
            return

        if message.content.find('<@!786278859775017061>') != -1 or message.content.find('<@786278859775017061>') != -1:
            await message.channel.send("My prefix here is `h.`")

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
                            self.reminders['h'], self.reminders['m'], self.reminders['s'] = int(hour), int(min), int(sec)
                        else:
                            self.reminders['h'], self.reminders['m'], self.reminders['s'] = 2, 0, 0
                
                        time = (self.reminders['h']*60 + self.reminders['m'])*60 + self.reminders['s'] # in seconds
                        msg1 = f"reminder is set for {self.reminders['h']}h {self.reminders['m']}m {self.reminders['s']}seconds....! <:teehee:775029757690773517>"
                        msg2 = '<@506018589904470047>, rpg guild raid/upgrade is ready....!'

                        await self.reminder(time, channelId, msg1, msg2, 'guildRem') 
    
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
                        
                        response = requests.get("https://complimentr.com/api")
                        complimentb = response.content.decode("UTF-8")
                        compliment = ast.literal_eval(complimentb)

                        msg1 = personBumped + ', Ty for bumping'
                        if compliment["compliment"]:
                             msg1 += ' and ' + compliment['compliment']
                        await message.channel.send(msg1)

                    elif description.find('Please wait another') != -1:
                        temps0, temps1 = description.split(', Please wait another ')
                        temps2 = list(temps1.split())
                        minutes = int(temps2[0])

                    #time = minutes*60 # in seconds
                    #msg2 = '<@506018589904470047>, you can bump the server again....!'
                    #await self.reminder(time,channelId,msg1, msg2, which = 'bump'+str(channelId))
    
        # Special Trades / Random event drops
        if message.author.id == 555955826880413696: # Epic RPG Bot ID
            if len(message.embeds) > 0:
                embed = message.embeds[0]
                if len(embed.fields) >0:
                    fields = embed.fields[0]
                    if fields.value.find('The first player who types the following sentence will get') != -1:
                        playerMsg, rewardMsg = fields.value.split('\n')
                        await message.channel.send(rewardMsg)
                        await owner.send(f"special trade - https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}\n - Triggered by: {message.author.name} in <#{message.channel.id}>")
    

def setup(bot):
   bot.add_cog(Miscellaneous(bot))