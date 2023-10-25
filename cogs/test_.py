import discord
from discord.ext import commands

class test_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def test(self, ctx):
        await ctx.respond("Успешный тест")

    @commands.slash_command()
    async def lol(self, ctx):
        await ctx.respond("Gjitk d gbple vhfpm") # я знаю что тут написано :moon_face:

    @bot.slash_command(name='тест', description='Что-то делает.', guild_ids=None)
    async def test_(ctx):
        await ctx.respond('Успешный тест!')

def setup(bot):
    bot.add_cog(test_(bot))
