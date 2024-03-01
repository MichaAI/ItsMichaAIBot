import random

import aiohttp
import discord
from discord.ext import commands

with open("./commands/rm.txt") as file:
    rm_help = file.read()


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["Привет", "привет"])
    async def hi(self, ctx):
        await ctx.reply(f"Здравствуй, {ctx.message.author.mention}!")

    @commands.command(aliases=["bаn", "бaн"])
    async def banan(self, ctx, *, reason: str = "None"):
        if not ctx.message.reference:
            return
        original = await ctx.fetch_message(ctx.message.reference.message_id)
        await ctx.reply(
            f"Пользователь {original.author.mention} был забанен пользователем {ctx.message.author.mention} по причине `{reason}`"
        )

    @commands.command(aliases=["взорвался"])
    async def explode(self, ctx: discord.ApplicationContext):
        msg = []
        async for message in ctx.channel.history(limit=100):
            if message.author == ctx.message.author:
                continue
            if message.author in msg:
                continue
            msg.append(message.author)
        parts = [
            "прилетела голова",
            "прилетела правая рука",
            "прилетела левая рука",
            "прилетела правая нога",
            "прилетела левая нога",
            "прилетело туловище",
            "прилетело сердце",
            "прилетели глаза",
            "прилетел мозг",
            "прилетел язык",
            "прилетела печень",
            "прилетел желудок",
            "прилетели лёгкие",
        ]
        msg = msg[: len(parts) - 1]
        exploded = ""
        for i in range(random.randint(2, 10)):
            safety_limit = 100
            _ = 0
            while _ < safety_limit:
                part = random.choice(parts)
                _ += 1
                if part in exploded:
                    continue
                exploded += f"**В {random.choice(msg).mention} {part}**\n"
                break
        await ctx.reply(
            f"**{ctx.message.author.mention} взорвался!**\n" + exploded.strip(),
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @commands.command(aliases=["rm"])
    async def rm_(self, ctx, flags: str = None, directory: str = None):
        if not flags and not directory:
            await ctx.reply(
                "rm: missing operand \n" "Try 'rm --help' for more information."
            )
            return

        if flags == "--help":
            await ctx.reply(rm_help)
            return

        if not flags.startswith("-"):
            if directory:
                await ctx.reply(f"Файлы {flags} и {directory} успешно удаленны")
                return
            await ctx.reply(f"Файл {flags} успешно удаллен")
            return

        if flags == "-rf" and directory == "/*":
            await ctx.reply("Система успешно удаленна! Удачного дня!")
            return

        if "r" in flags:
            await ctx.reply(f"Директория {directory} успешно удаленна!")
            return

        await ctx.reply(f"Файл {directory} успешно удаленн!")

    @commands.command()
    async def joke(self, ctx: commands.Context):
        async with aiohttp.ClientSession() as session:
            response = await session.get(
                url="https://official-joke-api.appspot.com/random_joke",
            )
            response = await response.json()
        embed = discord.Embed(title="Joke:")
        embed.add_field(name=response["setup"], value=f'||{response["punchline"]}||')
        embed.set_footer(text=f'Type: {response["type"]}; ID: {response["id"]}')
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
