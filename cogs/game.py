import discord
from discord.ext import commands

class game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def Game(self, ctx):
        await ctx.reply(f"Игра возможно скоро будет готова, {ctx.message.author.mention}")

def setup(bot):
    bot.add_cog(game(bot))