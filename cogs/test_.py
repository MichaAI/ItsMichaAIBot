from discord.ext import commands


class TestTest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def test_(self, ctx):
        await ctx.respond("Успешный тест!")


def setup(bot):
    bot.add_cog(TestTest(bot))
