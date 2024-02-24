import random
import discord
from discord.ext import commands
from redis import asyncio as aioredis
from math import ceil, log2

r = aioredis.StrictRedis(host="localhost", port=6379, decode_responses=True)

class Pseudoai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.is_nsfw()
            return

        msg_split = message.content.split()
        content = {i:msg_split.count(i) for i in msg_split}

        for key, value in content.items():
            ttl = await r.ttl(key)
            await r.set(key, 0, 600*value + ttl)
        
        if message.author == self.bot.user:
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
