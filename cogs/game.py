import discord
from discord.ext import commands
from game_logic.game_generate import generate_game
from game_logic.game_dbwork import game_get_from_db


class game_buttons(discord.ui.View):
    def __init__(self, author):
        self.author = author
        super().__init__()

    @discord.ui.button(label='⏫', style=discord.ButtonStyle.green)
    async def up_button(self, button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            r, g = game_get_from_db(interaction.user.id)
            await interaction.response.edit_message(content=f'{r} and {g}')
        else:
            await interaction.response.send_message(content='Вы не можете контактировать с чужими играми! '
                                                            'Вызовите свою игру с помощью комманды!',
                                                    ephemeral=True)


class game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def game_test(self, ctx, seed: int, x: int, y: int):
        cave_map = generate_game(seed=seed, x_offset=x, y_offset=y)
        a = '\n'.join([''.join(str(cell) for cell in row) for row in cave_map])
        view = game_buttons(ctx.author)
        await ctx.respond(a, view=view)
        print(game_get_from_db(ctx.author.id))


def setup(bot):
    bot.add_cog(game(bot))
