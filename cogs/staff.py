import asyncio
import discord
from discord.ext import commands, menus
from helpers import pagination, checkers

# TODO
# membersinrole - convert idn to discord.guild.role and add command error handler

class Staff(commands.Cog):
    """
    tiny helpers to make life easy
    """
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases = ['mir'])
    async def membersinrole(self, ctx, *, idn:str = None, case_insensitive=True):
        """
        Gives list of users who have this role.
        **usage** 
        `h.mir <id/Name>`
        **Alias**
        mir
        """
        if not checkers.isStaff(ctx.message.author):
            await ctx.send("You are not part of LIMBO staff. you can't use this command.")
            return

        if idn is None:
            await ctx.send("Please enter role id / name")
            return

        rolesInServer = ctx.guild.roles
        try:
            idn = int(idn)
        except:
            idn = idn.lower()
    
        roleRequested = list(filter(lambda x: x.name.lower() == idn or int(x.id) == idn, rolesInServer))
        if not len(roleRequested):
            await ctx.send("that role id / name is not found in server.")
            return

        members = roleRequested[0].members
        if len(members) == 0:
            await ctx.send('There are no members in this role.')
            return

        async def get_page(pidx):
            thisPage = members[min(len(members), pidx*10) : min(len(members), pidx*10+10)]

            embed = discord.Embed(color=0xFCDCF5)
            embed.title = f'Role: {roleRequested[0].name} ({roleRequested[0].id})\n\n'
            embed.set_footer(text= f'page {pidx+1}/{(len(members)-1)//10+1}')

            description = f'**Members:**\n\n'
    
            for c,m in enumerate(thisPage, 1):
                description += f'**#{c+pidx*10} | {m.name}** ({m.id})\n\n'
            embed.description = description
            return embed
        
        paginator = pagination.Paginator(get_page, (len(members)-1) // 10 + 1)
        await paginator.send(ctx)
    
def setup(bot):
   bot.add_cog(Staff(bot))