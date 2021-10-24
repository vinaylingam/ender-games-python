import discord
from config import config 
from discord.ext import commands

def isOwner(member):
    return member.id is config._owner

def isAdmin(member):
    return isOwner(member) or member.guild_permissions.administrator

def isStaff(server, member):
    return isOwner(member) or member.guild_permissions.administrator or len(list(filter(lambda x: x.id in server.staff, member.roles)))