from discord.ext import commands
import discord


class StarRemove(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.guild_id != 1076117733428711434:
            return

        if payload.emoji != discord.PartialEmoji(name="⭐"):
            return
        message = await self.bot.get_channel(payload.channel_id).fetch_message(
            payload.message_id
        )
        star_reactions = list(filter(lambda r: r.emoij == "⭐", message.reactions))
        star_reaction = star_reactions[0]
        await star_reaction.clear()


def setup(bot):
    bot.add_cog(StarRemove(bot))
