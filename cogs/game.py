import discord
from discord.ext import commands
from game_logic.game_generate import generate_game
from game_logic.game_dbwork import game_get_from_db

class game_buttons(discord.ui.View):
    def __init__(self, author):
        self.author = author
        super().__init__()

    @discord.ui.button(emoji='⏫', style=discord.ButtonStyle.green)
    async def up_button(self, interaction: discord.Interaction):
        if interaction.user.id == self.author:
            await interaction.response.edit_messade(content='⏫', view=self)
        else:
            await interaction.response.send_messade(content='Вы не можете контактировать с чужими играми! '
                                                            'Вызовите свою игру с помощью комманды!')

class game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def game_test(self, ctx, seed: int, x: int, y: int):
        cave_map = generate_game(seed=seed, x_offset=x, y_offset=y)
        a = '\n'.join([''.join(str(cell) for cell in row) for row in cave_map])
        await ctx.respond(a)
        print(game_get_from_db(ctx.author.id))


def setup(bot):
    bot.add_cog(game(bot))
