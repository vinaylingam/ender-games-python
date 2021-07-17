import discord
from discord.ext import commands

class Dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['mdwi'], hidden = True)
    async def messageDetailWithId(self, ctx, ch:discord.TextChannel, id:int = None, case_insensitive=True):

        message = await ch.fetch_message(id)
        
        await ctx.send(str(message.channel.id) + ' ' + str(message.id) + ' ' + str(message.author.name) + ' ' + str(message.content))
        await ctx.send(message)
        embeds = message.embeds
        for embed in embeds:
            await ctx.send(embed.to_dict())
            print(embed.to_dict())

def setup(bot):
   bot.add_cog(Dev(bot))