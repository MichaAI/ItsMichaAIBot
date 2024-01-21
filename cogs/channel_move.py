import typing
import discord
from discord.ext import commands


class ChannelMove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="переместить_канал",
        description="Перемещает канал вверх" "(вниз при отрицательных числах)",
    )
    async def move_channel(
        self,
        ctx,
        channel: typing.Union[
            discord.TextChannel,
            discord.VoiceChannel,
            discord.StageChannel,
            discord.ForumChannel,
        ],
        move_to: int,
    ):
        """Move channel lol"""
        if not (
            ctx.author.guild_permissions.manage_channels
            or ctx.author.guild_permissions.administrator
        ):
            return await ctx.respond("Недостаточно полномочий.")

        await channel.edit(position=channel.position - move_to)
        await ctx.respond(
            f"Позиция канала {channel.mention}"
            "успешно изменена на {abs(move_to)} каналов"
            '{"вверх" if move_to>0 else "вниз"}'
        )


def setup(bot):
    bot.add_cog(ChannelMove(bot))
