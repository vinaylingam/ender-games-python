import discord
from discord.ext import commands

async def reminder(bot, time, id, msgBeforeReminder = None, msgAfterReminder = None, which = None, where = 'Channel'):
    if where == 'Channel':
        remind = bot.get_channel(id)
    else: # DM's
        remind = bot.get_user(id)

    if which != '' and reminderStates[which] == True:
        return

    await remind.send(msgBeforeReminder)
    if which != '':
        self.reminderStates[which] = True
    await asyncio.sleep(time)
    await remind.send(msgAfterReminder)
    if which != '':
        self.reminderStates[which] = False