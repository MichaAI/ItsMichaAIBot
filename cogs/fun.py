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
        await ctx.reply(
            f"Пользователь {original.author.mention} был забанен пользователем {ctx.message.author.mention} по причине `{reason}`"
        )

    @commands.command(aliases=["взорвался"])
    async def boom(self, ctx: discord.ApplicationContext):
        msg = []
        async for message in ctx.channel.history(limit=6):
            msg.append(message)
        await ctx.reply(f"{ctx.message.author.mention} взовался! \n"
                  f"В {msg[0].author} прилетела правая рука! \n"
                  f"В {msg[1].author} прилетела левая рука! \n "
                  f"В {msg[2].author} прилетела правя нога! \n "
                  f"В {msg[3].author} прилетела левая нога! \n "
                  f"В {msg[4].author} прилетела голова! \n "
                  f"В {msg[4].author} прилетелo сердце! \n "
                  )

def setup(bot):
    bot.add_cog(Fun(bot))
