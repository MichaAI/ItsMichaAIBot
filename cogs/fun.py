import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["Привет", "привет"])
    async def hi(self, ctx):
        await ctx.reply(f"Здравствуй, {ctx.message.author.mention}!")


    @commands.command(aliases=["bаn", "бaн"])
    async def hi(self, ctx, *, reason: str = "None"):
        if not ctx.message.reference:
            return
        original = await ctx.fetch_message(ctx.message.reference.message_id)
        await ctx.reply(f"Пользователь {original.author.mention} был забанен пользователем {ctx.message.author.mention} по причине `{reason}`")


def setup(bot):
    bot.add_cog(Fun(bot))
