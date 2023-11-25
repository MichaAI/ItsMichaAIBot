import discord
from discord.ext import commands
from game_logic.game_generate import generate_game

class game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def Game(self, ctx, seed: int, x: int, y: int):
        cave_map = generate_game(seed=seed, x_offset=x, y_offset=y)
        a = '\n'.join([''.join(str(cell) for cell in row) for row in cave_map])
        await ctx.reply(a)

def setup(bot):
    bot.add_cog(game(bot))