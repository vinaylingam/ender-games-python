import discord
from discord.ext import commands

def isAdmin(member):
    return member.guild_permissions.administrator

def isStaff(server, member):
    if server.staff is None:
        return false
    return member.guild_permissions.administrator or len(list(filter(lambda x: x.id in server.staff, member.roles)))