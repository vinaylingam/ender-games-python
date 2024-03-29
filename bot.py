import discord
from discord.ext import commands, events
from config import KEYS
import asyncio
from datetime import datetime
from pytz import timezone
from collections import defaultdict
#import challonge

COGS = [
    'dev',
    'help',
    'miscellaneous',
    'staff',
    'channels',
    'mongo',
    'configuration'
    ]

class Bot(commands.AutoShardedBot, events.EventsMixin):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
            command_prefix= 'h.',
            case_insensitive=True,
            intents=discord.Intents.all(),
        )

        for i in COGS:
            self.load_extension(f"cogs.{i}")
    
    @property
    def mongo(self):
        return self.get_cog('Mongo')

    def printTime():
        format = "%Y-%m-%d %H:%M:%S %Z%z"
        utc = datetime.now(timezone('UTC'))
        ist = utc.astimezone(timezone('Asia/Kolkata'))
        return ist.strftime(format)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        owner = self.get_user(506018589904470047)
        await owner.send("im up..! -")

if __name__ == "__main__":
    bot = Bot()
    bot.run(KEYS.discordToken)
