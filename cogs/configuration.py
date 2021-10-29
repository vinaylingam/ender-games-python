import discord
from discord.ext import commands
from helpers import checkers

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(case_insensitive=True)
    async def settings(self,ctx):
        """
        configurations of the server.
        **Usage**
        h.settings
        **Alias**
        None
        """
        server = await self.bot.mongo.fetch_server_info(ctx.message.guild)
        if server is None or server.staff is None:
            await ctx.send("Server staff are not assigned, Please ask the admin to add staff (command: `addstaff`)")
            return
        elif not checkers.isStaff(server, ctx.message.author):
            await ctx.send("only staff can do this command")
            return

        serverSettings = await self.bot.mongo.fetch_server_info(ctx.message.guild)
        if serverSettings is None:
            await self.bot.mongo.update_server(ctx.message.guild, {'$set': { '_id':ctx.message.guild.id }})
            serverSettings = await self.bot.mongo.fetch_server_info(ctx.message.guild)
        
        embed = discord.Embed(color=0xFCDCF5, title=f'{ctx.message.guild.name} Settings')
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        descr = '**staff roles:** '
        descr += ', '.join(map(lambda x: '<@&'+str(x)+'>', serverSettings.staff)) if not serverSettings.staff is None and len(serverSettings.staff) >0 else ''
        descr += '\n'

        embed.description = descr
        await ctx.send(embed = embed)  
        
    @commands.command(aliases = ['addstaffroles', 'addstaffrole'], case_insensitive=True)
    async def addstaff(self, ctx, roles: commands.Greedy[discord.Role] = None):
        """
        Add staff roles to server.
        **Usage**
        h.addstaffrole <role1> <role2> <role3>...
        **Alias**
        addstaffroles, addstaffrole
        """
        if not (checkers.isAdmin(ctx.message.author) or checkers.isOwner(ctx.message.author)):
            await ctx.send("only admin can do this command")
            return

        if roles is None:
            await ctx.send("pls check `h.help addstaffrole`")
            return

        await self.bot.mongo.update_server(ctx.message.guild, {'$addToSet': {'staff': { '$each' : [ m.id for m in roles] }}})
        embed = discord.Embed(color=0xFCDCF5, title='Add staff')
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        rolepings = map(lambda x: '<@&'+str(x.id)+'>', roles)
        descr = ', '.join(rolepings) + ' are added as the staff for this server.'
        embed.description = descr
        await ctx.send(embed = embed)

    @commands.command(aliases = ['removestaffroles', 'removestaffrole'], case_insensitive=True)
    async def removestaff(self, ctx, roles: commands.Greedy[discord.Role] = None):
        """
        remove staff role from server.
        **usage**
        h.removestaff <role1> <role2> <role3>...
        **Alias**
        removestaffroles, removestaffrole
        """
        if not checkers.isAdmin(ctx.message.author):
            await ctx.send("only admin can do this command")
            return

        if roles is None:
            await ctx.send("pls check `h.help removestaff`")
            return

        await self.bot.mongo.update_server(ctx.message.guild, {'$pull': {'staff': { '$in' : [ m.id for m in roles] }}})
        embed = discord.Embed(color=0xFCDCF5, title='Remove staff')
        embed.set_author(name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url)

        rolepings = map(lambda x: '<@&'+str(x.id)+'>', roles)
        descr = ', '.join(rolepings) + ' are removed from staff.'
        embed.description = descr
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Configuration(bot))
