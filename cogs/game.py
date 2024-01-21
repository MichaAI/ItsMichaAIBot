import random
import discord
import importlib
import sys
from discord.ext import commands
from game_logic.game_generate import generate_game, find_start
from game_logic.game_dbwork import game_get_from_db, insert_to_db


class GameButtons(discord.ui.View):
    def __init__(self, author):
        self.author = author
        super().__init__()

    @discord.ui.button(label="⏫", style=discord.ButtonStyle.green)
    async def up_button(self, button, interaction: discord.Interaction):
        if interaction.user.id == self.author.id:
            r, g = game_get_from_db(interaction.user.id)
            await interaction.response.edit_message(content=f"{r} and {g}")
        else:
            await interaction.response.send_message(
                content="Вы не можете контактировать с чужими играми! "
                "Вызовите свою игру с помощью комманды!",
                ephemeral=True,
            )


class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def game_test(self, ctx):
        _, game_data = game_get_from_db(ctx.author.id)

        if game_data is None:
            await ctx.respond(
                f"Добро пожаловать, {ctx.author.mention}, вставте сюда обучение нахуй,"
                f" используйте комманду еще раз что бы начать игру"
            )
            # ваще хз че сюда можно вставить кроме этого
            seed = random.randint(0, 24009090900)
            x = find_start(seed)
            insert_to_db(ctx.author.id, seed, x, to_mongo=True)
        else:
            cave_map = generate_game(
                seed=game_data["seed"], x_offset=game_data["x"], y_offset=game_data["y"]
            )
            a = "\n".join(["".join(str(cell) for cell in row) for row in cave_map])
            view = GameButtons(ctx.author)
            await ctx.respond(a, view=view)
            insert_to_db(**game_data)


def setup(bot):
    bot.add_cog(Game(bot))


# pylint: disable=unused-argument


def teardown(bot):
    print("[I] [Game] Cog unloading! Cleaning up...")
    print(importlib.reload(sys.modules["game_logic.game_generate"]))
    print(importlib.reload(sys.modules["game_logic.game_dbwork"]))


# pylint: enable=unused-argument
