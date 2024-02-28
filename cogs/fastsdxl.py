import json
import aiohttp
import discord
from discord.ext import commands


class Fastsdxl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["image"])
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def fastsdxl_command(self, ctx: commands.Context, *, promt: str):
        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url="https://fal.run/fal-ai/fast-lightning-sdxl",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Key {self.bot.fal_key}",
                },
                data=json.dumps({"prompt": promt, "enable_safety_checker": True}),
            )
            response = await response.json()

        if ctx.channel.nsfw:
            await ctx.reply(response["images"][0]["url"])
            return
        if not any(response["has_nsfw_concepts"]):
            await ctx.reply(response["images"][0]["url"])
            return
        await ctx.reply("Ай как плохо такое генерировать")

    @commands.slash_command(name="image", description="fast image generator")
    @commands.cooldown(2, 10, commands.BucketType.user)
    async def move_channel(
        self, ctx, promt: str, number_images: int = 1, negative: str = ""
    ):
        if number_images > 4:
            await ctx.respond(
                "Слишком много изображений, макксимум `4` изображения в одном запросе",
                ephimeral=True,
            )
            return

        async with aiohttp.ClientSession() as session:
            response = await session.post(
                url="https://fal.run/fal-ai/fast-lightning-sdxl",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Key {self.bot.fal_key}",
                },
                data=json.dumps(
                    {
                        "prompt": promt,
                        "num_images": number_images,
                        "negative_prompt": negative,
                        "enable_safety_checker": True,
                    }
                ),
            )
        response = await response.json()
        if ctx.channel.nsfw:
            await ctx.respond(
                " ".join(
                    [
                        response["images"][x]["url"]
                        for x in range(len(response["images"]))
                    ]
                )
            )

            return
        if not any(response["has_nsfw_concepts"]):
            await ctx.respond(
                " ".join(
                    [
                        response["images"][x]["url"]
                        for x in range(len(response["images"]))
                    ]
                )
            )
        await ctx.respond("Ой как плохо такое генерировать, осуждаю.", ephimeral=True)


def setup(bot):
    bot.add_cog(Fastsdxl(bot))
