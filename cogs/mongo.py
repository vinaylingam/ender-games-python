import discord
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient
from umongo import Document, EmbeddedDocument, Instance, MixinDocument, fields
from umongo.frameworks import MotorAsyncIOInstance
from config import KEYS

class Member(Document):
    class Meta:
        collection_name = 'member'

    id = fields.IntegerField(attribute="_id")
    channelOwned = fields.IntegerField(default = None)
    sid = fields.IntegerField(default=None)

class Channel(Document):
    class Meta:
        collection_name = 'channel'

    id = fields.IntegerField(attribute='_id', unique = True)
    owners = fields.ListField(fields.IntegerField())
    claimType = fields.StrField(default = '')
    
class Mongo(commands.Cog):
    """
    for database operations.
    """

    def __init__(self,bot):
        self.bot = bot
        self.client = AsyncIOMotorClient(KEYS.DATABASE_URI, io_loop=bot.loop)
        self.db = self.client[KEYS.DATABASE_NAME]
        
        instance = MotorAsyncIOInstance(self.db)
        self.Member = instance.register(Member)
        self.Channel = instance.register(Channel)

    async def fetch_member_info(self, member: discord.Member, guild: discord.Guild):
        mem = await self.Member.find_one({"_id": member.id})
        return mem

    async def fetch_channel_info(self, ch: discord.TextChannel):
        chh = await self.Channel.find_one({"_id": ch.id})
        return chh

    async def update_member(self, member: discord.Member, guild : discord.Guild, update):
        result = await self.db.member.update_one({"_id": member.id, 'sid':guild.id}, update, upsert=True)
        return result

    async def update_channel(self, channel: discord.TextChannel, update):
        result = await self.db.channel.update_one({"_id": channel.id}, update, upsert=True)
        return result

def setup(bot):
    bot.add_cog(Mongo(bot))