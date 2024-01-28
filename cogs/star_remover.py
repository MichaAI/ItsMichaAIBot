from discord.ext import commands
import discord


class StarRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id != 1076117733428711434:
            return

        message = await self.bot.get_channel(payload.channel_id).fetch_message(
            payload.message_id
        )

        for reaction in message.reactions:
            if reaction.emoji != "⭐":
                continue
            await reaction.clear()


def setup(bot):
    bot.add_cog(StarRemove(bot))
