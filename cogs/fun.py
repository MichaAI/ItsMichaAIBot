import discord
import random
from discord.ext import commands


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

    @commands.command(aliases=["настроение"])
    async def mood(self, ctx):
        await ctx.reply(f"Настроение испорченно...")


def setup(bot):
    bot.add_cog(Fun(bot))
