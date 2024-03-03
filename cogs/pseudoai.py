import asyncio
import random
import string

import discord
from discord.ext import commands
from redis import asyncio as aioredis

r = aioredis.StrictRedis(host="redis1", port=6380, db=0, decode_responses=True)


class Pseudoai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        if message.author == self.bot.user:
            return

        msg_split = message.content.split()
        content = {i: msg_split.count(i) for i in msg_split}

        asyncio.create_task(self.redis_inserting(content))

        if message.channel.id not in (
            1076117734208835606,
            1106541600034783332,
            1073641946129641584,
        ):
            return

        if random.randint(1, 30) != 1:
            return

        keys = await self.redis_geting()
        await message.channel.send(
            keys,
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @commands.command()
    async def random_phrase(self, ctx):
        keys = await self.redis_geting()
        await ctx.reply(
            keys,
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @staticmethod
    async def redis_inserting(content: dict) -> None:
        for key, value in content.items():
            if "http" in key:
                continue
            ttl = await r.ttl(key)
            key2 = key.lower().translate(str.maketrans('', '', string.punctuation))
            if not key2:
                continue
            await r.set(
                key2, 0, (600 * value) + ttl
            )

    @staticmethod
    async def redis_geting():
        keys = ""

        for _ in range(random.randint(1, 4)):
            sentence = ""
            for _ in range(random.randint(3, 10)):
                sentence += await r.randomkey() + ""
            keys += " " + sentence[0].upper() + sentence[1:] + random.choice(".!?")

        return keys


def setup(bot):
    bot.add_cog(Pseudoai(bot))
