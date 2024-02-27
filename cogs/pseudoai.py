import random
import discord
from discord.ext import commands
from redis import asyncio as aioredis


r = aioredis.StrictRedis(host="redis1", port=6380, db=0, decode_responses=True)


class Pseudoai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        msg_split = message.content.split()
        content = {i: msg_split.count(i) for i in msg_split}

        for key, value in content.items():
            ttl = await r.ttl(key)
            await r.set(key, 0, 600 * value + ttl)

        if message.author == self.bot.user:
            return

        if message.channel.id not in (
            1076117734208835606,
            1106541600034783332,
            1073641946129641584,
        ):
            return

        if random.randint(1, 30) != 1:
            return

        keys = []

        for _ in range(random.randint(5, 15)):
            key = await r.randomkey()
            keys.append(key)
            ttl = await r.ttl(key)
            await r.expire(key, ttl - 1)

        await message.channel.send(" ".join(keys))


def setup(bot):
    bot.add_cog(Pseudoai(bot))
