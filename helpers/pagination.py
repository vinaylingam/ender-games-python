﻿import asyncio
import discord
from discord.ext import commands, menus


class AsyncListPageSource(menus.AsyncIteratorPageSource):
    def __init__(self, data, title=None, show_index=False, format_item=str):
        super().__init__(data, per_page=20)
        self.title = title
        self.show_index = show_index
        self.format_item = format_item

    async def format_page(self, menu, entries):
        lines = (
            f"{i+1}. {self.format_item(x)}" if self.show_index else self.format_item(x)
            for i, x in enumerate(entries, start=menu.current_page * self.per_page)
        )
        return discord.Embed(
            title=self.title,
            color=0xFCDCF5,
            description=f"\n".join(lines),
        )

class AsyncFieldsPageSource(menus.AsyncIteratorPageSource):
    def __init__(self, data, title=None, count=None, format_item=lambda i, x: (i, x)):
        super().__init__(data, per_page=5)
        self.title = title
        self.format_item = format_item
        self.count = count

    async def format_page(self, menu, entries):
        embed = discord.Embed(
            title=self.title,
            color=0xFCDCF5,
        )
        start = menu.current_page * self.per_page
        i = start
        for i, x in enumerate(entries, start=start):
            embed.add_field(**self.format_item(i, x))
        footer = f"Showing entries {start+1}–{i+1}"
        if self.count is not None:
            footer += f" out of {self.count}"
        embed.set_footer(text=footer)
        return embed

class Paginator:
    def __init__(self, get_page, num_pages):
        self.num_pages = num_pages
        self.get_page = get_page

    async def send(self, ctx: commands.Context, pidx: int = 0):

        embed = await self.get_page(pidx)
        message = await ctx.send(embed=embed)

        if self.num_pages > 1:
            await message.add_reaction("⏮️")
            await message.add_reaction("◀")
            await message.add_reaction("▶")
            await message.add_reaction("⏭️")
        await message.add_reaction("\N{wastebasket}")

        try:
            while True:
                reaction, user = await ctx.bot.wait_for(
                    "reaction_add",
                    check=lambda r, u: r.message.id == message.id
                    and u.id == ctx.author.id,
                    timeout=120,
                )
                try:
                    await reaction.remove(user)
                except:
                    pass

                if reaction.emoji == "\N{wastebasket}":
                    await message.delete()
                    return

                else:
                    pidx = {
                        "⏮️": 0,
                        "◀": pidx - 1,
                        "▶": pidx + 1,
                        "⏭️": self.num_pages - 1,
                    }[reaction.emoji] % self.num_pages

                embed = await self.get_page(pidx)
                await message.edit(embed=embed)

        except asyncio.TimeoutError:
            await message.add_reaction("❌")