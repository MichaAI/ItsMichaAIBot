import asyncio
import random
import discord
from discord.ext import commands
from redis import asyncio as aioredis


r = aioredis.StrictRedis(host="redis1", port=6380, db=0, decode_responses=True)


class Pseudoai(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        msg_split = message.content.split()
        content = {i: msg_split.count(i) for i in msg_split}

        for key, value in content.items():
            asyncio.create_task(self.redis_inserting(key, value))

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
        
        keys = await self.redis_geting()
        await message.channel.send(" ".join([str(x) for x in keys]))
    
    @commands.command()
    async def random_phrase(self, ctx):
        keys = await self.redis_geting()
        await ctx.reply(" ".join([str(x) for x in keys]), allowed_mentions=discord.AllowedMentions.none())

    @staticmethod
    async def redis_inserting(key: str, value: int) -> None:
        if key[0].isupper() and key[-1] in ".?!‽¡":
            await r.hset("start-end", key, key)
            return None
        if key[0].isupper():
            await r.hset("start", key, key)
            return None
        if key[-1] in ".?!‽¡":
            await r.hset("end", key, key)
            return None
        ttl = await r.ttl(key)
        await r.set(key, 0, (600 * value) + ttl)

    @staticmethod
    async def redis_geting() -> list[str]:
        keys = []

        for _ in range(random.randint(1, 4)):
            if random.randint(1, 7) == 7:
                st_end = await r.hrandfield("start-end")
                keys.append(st_end)

            start = await r.hrandfield("start")
            keys.append(start)

            for _ in range(random.randint(3, 10)):
                key = await r.randomkey()
                keys.append(key)
                ttl = await r.ttl(key)
                await r.expire(key, ttl - 1)

            end = await r.hrandfield("end")
            keys.append(end)

        return keys


def setup(bot):
    bot.add_cog(Pseudoai(bot))
