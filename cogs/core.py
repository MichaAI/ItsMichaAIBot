import discord
from discord.ext import commands

class core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @bot.slash_command()
    @commands.is_owner()
    async def reload_cogs(ctx):
        for f in os.listdir("./cogs"):
            if not f.endswith(".py"): continue
            if "cogs." + f[:-3] in bot.extensions:
                bot.unload_extension("cogs." + f[:-3])
                bot.load_extension("cogs." + f[:-3])
            else:
                bot.load_extension("cogs." + f[:-3])
            await ctx.send("cogs." + f[:-3] + ' reloaded')
          

def setup(bot):
    bot.add_cog(test_(bot))
