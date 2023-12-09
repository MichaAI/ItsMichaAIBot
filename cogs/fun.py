import discord
from discord.ext import commands


class fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["Привет", "привет"])
    async def hi(self, ctx):
        await ctx.reply(f"Здравствуй, {ctx.message.author.mention}")


def setup(bot):
    bot.add_cog(fun(bot))
