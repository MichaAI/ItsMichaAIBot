import random
import discord
from discord.ext import commands
from game_logic.game_generate import generate_game, find_start
from game_logic.game_dbwork import game_get_from_db, insert_to_db, r


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
    async def game_test(self, ctx):
        redis, game = game_get_from_db(ctx.author.id)

        if game is None:
            await ctx.respond(f'Добро пожаловать, {ctx.author.mention}, вставте сюда обучение нахуй,'
                              f' используйте комманду еще раз что бы начать игру')
            seed = random.randint(0, 24009090900)  # ваще хз че сюда можно вставить кроме этого
            x = find_start(seed)
            insert_to_db(ctx.author.id, seed, x, to_mongo=True)
            return
        else:
            cave_map = generate_game(seed=game['seed'], x_offset=game['x'], y_offset=game['y'])
            a = '\n'.join([''.join(str(cell) for cell in row) for row in cave_map])
            view = game_buttons(ctx.author)
            await ctx.respond(a, view=view)




def setup(bot):
    bot.add_cog(game(bot))
