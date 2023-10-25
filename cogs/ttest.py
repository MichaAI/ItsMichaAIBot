import discord
from discord.ext import commands

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def test(self, ctx):
        await ctx.respond("Успешный тест")

    @commands.slash_command()
    async def lol(self, ctx):
        await ctx.respond("Gjitk d gbple vhfpm")

def setup(bot):
    bot.add_cog(test(bot))