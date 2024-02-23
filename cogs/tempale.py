import discord
from discord.ext import commands


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["template"])
    async def template(self, ctx):
        await ctx.reply("template cog message")

    @commands.slash_command(name="template", description="template cog command")
    async def move_channel(self, ctx):
        await ctx.respond("template cog slash command message", ephimeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        pass


def setup(bot):
    bot.add_cog(Template(bot))
