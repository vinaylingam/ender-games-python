import discord
from discord.ext import commands

def isStaff(member):
    return member.guild_permissions.administrator or len(list(filter(lambda x: x.name.lower() == 'moderator' or x.name.lower() == 'helper', member.roles)))