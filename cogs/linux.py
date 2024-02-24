import discord
from discord.ext import commands
from redis import asyncio as aioredis

r = aioredis.StrictRedis(host="localhost", port=6379, decode_responses=True)

class Linux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pwd(self, ctx: commands.Context):
        directory = r.get("user_" + str(ctx.message.author.id))

        if directory != None:
            return await ctx.reply(directory)

        await r.set("user_" + str(ctx.message.author.id), "/", 3600)
        await ctx.reply("/")
        return "/"

    @commands.command()
    async def cd(self, ctx: commands.Context, directory: str):
        if not directory.startswith("/"):
            tmp = await r.get("user_" + str(ctx.message.author.id))
            if not tmp:
                tmp = "/"
            directory = tmp + directory
        if await r.hget(directory, ".") == "SELF_DIRECTORY":
            r.set("user_" + str(ctx.message.author.id), directory, 3600)
            await ctx.reply("** **")

    @commands.command()
    async def ls(self, ctx: commands.Context, flags:str = None, directory:str = None):
        if not flags and not directory:
            w = await rhgett(name=directory, key=".")
            print(w)
    
    @commands.command()
    async def echo(self, ctx: commands.Context, echo_string: str = "** **"):
        await ctx.reply(echo_string, allowed_mentions=discord.AllowedMentions.none(),)




def setup(bot):
    bot.add_cog(Linux(bot))
