import discord
from discord.ext import commands
import asyncio
import helpers

class channels(commands.Cog, name = "channel management"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['vo', 'verifyowners', 'verifyowner'], case_insensitive=True)
    async def verifyownership(self, ctx, members: commands.Greedy[discord.Member] = None):
        """
        returns channel name if you own any.
        **Usage**
        h.vo [discord_user]
        **Alias**
        vo
        """
        channelOwners = []
        notChannelOwners = []

        if members is None:
            await ctx.send('Please enter members.')
            return

        for member in members:
            memInfo = await self.bot.mongo.fetch_member_info(member, ctx.message.guild)
            if memInfo is None:
                await self.bot.mongo.update_member(member, ctx.mesage.guild, {'$set': {'channelOwned': None, 'sid':ctx.message.guild.id}})
                memInfo = await self.bot.mongo.fetch_member_info(member, ctx.message.guild)
            if memInfo.channelOwned is None:
                notChannelOwners.append(f' <@{member.id}>')
            else:
                channelOwners.append(f'<@{member.id}> is owner of <#{memInfo.channelOwned}>')

        descr = ' '
        if len(channelOwners) > 0:
            descr += '\n'.join(channelOwners) + '\n\n'
        if len(notChannelOwners) > 0:
            descr += ','.join(notChannelOwners)
            descr += ' don\'t own any channels.\n\n'

        embed = discord.Embed(color=0xFCDCF5, title='Ownership status')
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.description = descr
        await ctx.send(embed = embed)


    @commands.command(aliases = ['ci'], case_insensitive=True)
    async def channelinfo(self, ctx, ch: discord.TextChannel = None):
        """
        gives Number of owners of mentioned channel and their last message.
        """
        if ch is None:
            ch = ctx.message.channel
        resCh = await self.bot.mongo.fetch_channel_info(ch)

        descr = ''

        descr += f'**Claim type:** {resCh.claimType}\n\n'
        if len(resCh.owners) == 0:
            descr += '**No owners for this channel**'
        else:
            descr += '**Owners**\n'
            for idx, mem in enumerate(resCh.owners):
                memb = ctx.guild.get_member(mem)
                descr += f':small_blue_diamond: {memb.name} ({memb.id})\n'
        
        embed = discord.Embed(color=0xFCDCF5, title='Channel Info')
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.description = descr
        message = await ctx.send(embed = embed)

    @commands.command(alias = ['addowners'], case_insensitive=True)
    async def addowner(self, ctx, ch: discord.TextChannel, members: commands.Greedy[discord.Member]):
        """
        Add owners to the given channel.
        *Usage**
        h.addowner <channel> <user_1> <user_2> ...
        **Alias**
        None
        """
        notChannelOwners = []
        channelOwners = []

        for member in members:
            memInfo = await self.bot.mongo.fetch_member_info(member, ctx.message.guild)
            if memInfo is None:
                await self.bot.mongo.update_member(member, ctx.message.guild, {'$set': {'channelOwned': None, 'sid':ctx.message.guild.id}})
                memInfo = await self.bot.mongo.fetch_member_info(member, ctx.message.guild)
            if memInfo.channelOwned is None:
                notChannelOwners.append(member)
            else:
                channelOwners.append(f'<@{member.id}> is owner of <#{memInfo.channelOwned}>')
        
        descr = ' '
        if len(channelOwners) > 0:
            descr += '\n'.join(channelOwners) + '\n\n'
        if len(notChannelOwners) == 0:
            descr += 'All mentioned members own atleast one channel.'
        else:
            descr += 'do you wish to add '
            for idx, mem in enumerate(notChannelOwners):
                descr += f'<@{mem.id}>' if idx == 0 else f', <@{mem.id}>'
            descr += f' as owner/s of channel <#{ch.id}>?'
        
        embed = discord.Embed(color=0xFCDCF5, title='Add owners')
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)
        embed.description = descr
        message = await ctx.send(embed = embed)

        if len(notChannelOwners) != 0:
            await message.add_reaction('\U00002705')
            await message.add_reaction('\U0000274c')

            try:
                while True:
                    reaction, user = await ctx.bot.wait_for(
                        "reaction_add",
                        check=lambda r, u: r.message.id == message.id
                        and u.id == ctx.author.id,
                        timeout=120,
                    )
                    if reaction.emoji == "\U00002705":
                        embed.color = 0x00FF00
                        descr += '\n\n**members added to channel succesfully**'
                        
                        await self.bot.mongo.update_channel(ch, {'$push': {'owners': { '$each' : [ m.id for m in notChannelOwners] }}})
                        for mem in notChannelOwners:
                            await self.bot.mongo.update_member(mem, ctx.message.guild, {'$set': { 'channelOwned': ch.id }})
                        embed.description = descr
                        await message.edit(embed = embed)
                        break
                        
                    elif reaction.emoji == "\U0000274c":
                        embed.color = 0xFF0000
                        descr += '\n\n **Adding ownership cancelled**.'
                        embed.description = descr
                        await message.edit(embed = embed)
                        break

            except asyncio.TimeoutError:
                embed.color = 0xFF0000
                descr += '\n\n **Adding ownership cancelled**.'
                embed.description = descr
                await message.edit(embed = embed)       

    @addowner.error
    async def addowner_error(self, ctx, error):
        await ctx.send(f'you either missed mentioning channel or the member. pls check `h.help addowner`')
    
    @commands.command(case_insensitive=True)
    async def setChannelType(self, ctx, ch:discord.TextChannel = None, ctype = None):
        """
        Set the type of claim type :- booster or normal
        **usage**
        h.setchanneltype <channel> [claim type]
        **Alias**
        None
        """
        if ch == None:
            ch = ctx.message.channel

        try:
            await self.bot.mongo.update_channel(ch, {'$set': { 'claimType' : ctype }})
            await ctx.send("channel claim type is set.")
        except Exception as e:
            await ctx.send(e)

    @commands.command(case_insensitive=True)
    async def pin(self, ctx, mid = None):
        """
        pin a message if you are owner of channel / staff member
        **usage**
        h.ping <message_id>
        **Alias**
        None
        """
        mem = ctx.guild.get_member(ctx.author.id)

        message = await ctx.message.channel.fetch_message(mid)
        resCh = await self.bot.mongo.fetch_channel_info(ctx.message.channel)
        
        if mem.id in resCh.owners:
            await message.pin()
            await ctx.message.add_reaction('\U00002705')
        else:
            await ctx.send("you are not owner of this channel nor the staff member")

def setup(bot):
    bot.add_cog(channels(bot))