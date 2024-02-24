import random
import discord
from discord.ext import commands
from redis import asyncio as aioredis
from math import ceil, log2

r = aioredis.StrictRedis(host="redis1", port=6380, db=0, decode_responses=True)


class Template(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        msg_split = message.content.split()
        content = {i: msg_split.count(i) for i in msg_split}

        for key, value in content.items():
            await r.set(key, 0, 600 * value)

        if message.author == self.bot.user:
            return

        if random.randint(1, 20) != 1:
            return

        key_count = await r.dbsize()
        keys = []

        for _ in range(ceil(log2(key_count)) + 2):
            key = await r.randomkey()
            keys.append(key)
            ttl = await r.ttl(key)
            await r.expire(key, ttl - 1)

        await message.channel.send(" ".join(keys))


def setup(bot):
    bot.add_cog(Template(bot))
