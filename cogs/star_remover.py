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
            should_clear = True
            for user in reaction.users():
                if user.id not in [629999906429337600, 609348530498437140, 639066140957736971]: should_clear = False
            if not should_clear: continue
            await reaction.clear()


def setup(bot):
    bot.add_cog(StarRemove(bot))
