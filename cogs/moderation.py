import asyncio
import datetime

import discord
from discord.ext import commands


def parse(s):
    fmt = "".join("%" + c.upper() + c for c in "hms" if c in s)
    return datetime.datetime.strptime(s, fmt).time()


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.mutes = {}
        self.bot.moderation_cog = self
        self.db_client = self.bot.dbclient

        async def _unmute_after(bot, mute, guild):
            role = discord.utils.get(guild.roles, id=mute["role_id"])
            user = discord.utils.get(guild.members, id=mute["user_id"])
            if mute["start"] + mute["time"] < datetime.datetime.now().timestamp():
                await user.remove_roles(role)
                return

            await asyncio.sleep(
                (mute["start"] + mute["time"]) - datetime.datetime.now().timestamp()
            )
            await user.remove_roles(role)

        for guild in bot.guilds:
            mutes = list(self.db_client.mutes.data.find({"guild_id": guild.id}))
            if len(mutes) == 0:
                self.db_client.mutes.data.insert_one({"guild_id": guild.id, "data": []})
                mutes = self.db_client.mutes.data.find({"guild_id": guild.id})
            bot.mutes[guild.id] = mutes[0].get("data", [])
            for mute in bot.mutes[guild.id]:
                print(mute)
                asyncio.create_task(_unmute_after(bot, mute, guild))

    def sync_db(self, target_guild_id):
        mutes = list(self.db_client.mutes.data.find({"guild_id": target_guild_id}))
        if len(mutes) == 0:
            self.db_client.mutes.data.insert_one(
                {"guild_id": target_guild_id, "data": []}
            )
            mutes = self.db_client.mutes.data.find({"guild_id": target_guild_id})
        mutes = mutes[0]
        self.db_client.mutes.data.update_one(
            {"guild_id": target_guild_id},
            {"$set": {"data": self.bot.mutes.get(target_guild_id, [])}},
        )

    @commands.slash_command()
    async def set_mute_role(self, ctx, role: discord.Role):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond(
                embed=discord.Embed(
                    title="Недостаточно полномочий.",
                    description="Вам не хватает прав для исполнения команды.",
                    color=discord.Color.from_rgb(255, 0, 0),
                )
            )
            return
        mute_role_id = role.id
        server_id = ctx.guild.id
        mutes_config = list(self.db_client.mutes.config.find({"guild_id": server_id}))
        if len(mutes_config) == 0:
            self.db_client.mutes.config.insert_one(
                {"guild_id": server_id, "role_id": -1}
            )
            mutes_config = self.db_client.mutes.config.find({"guild_id": server_id})
        mutes_config = mutes_config[0]
        if mutes_config["role_id"] == mute_role_id:
            await ctx.respond(
                embed=discord.Embed(
                    title="Равное значение.",
                    description="Установленная роль мьюта равна данной.",
                    color=discord.Color.from_rgb(255, 0, 0),
                )
            )
            return
        self.db_client.mutes.config.update_one(
            {"guild_id": server_id}, {"$set": {"role_id": mute_role_id}}
        )
        await ctx.respond(
            embed=discord.Embed(
                title="Успех!",
                description="Роль мьюта установлена.",
                color=discord.Color.from_rgb(0, 255, 0),
            )
        )

    @commands.slash_command()
    async def mute(
        self,
        ctx,
        user: discord.Member,
        mute_time: str = "12h0m0s",
        reason: str = "Не указана",
    ):
        if not (
            ctx.author.guild_permissions.mute_members
            or ctx.author.guild_permissions.administrator
        ):
            await ctx.respond(
                embed=discord.Embed(
                    title="Недостаточно полномочий",
                    description="Вам не хватает прав для исполнения команды.",
                    color=discord.Color.from_rgb(255, 0, 0),
                )
            )
            return
        server_id = ctx.guild.id
        mutes_config = list(self.db_client.mutes.config.find({"guild_id": server_id}))
        if len(mutes_config) == 0:
            self.db_client.mutes.config.insert_one(
                {"guild_id": server_id, "role_id": -1}
            )
            mutes_config = self.db_client.mutes.config.find({"guild_id": server_id})
        mutes_config = mutes_config[0]
        mute_role_id = mutes_config["role_id"]
        if mute_role_id == -1:
            await ctx.respond(
                embed=discord.Embed(
                    title="Неверная конфигурация",
                    description="Роль мьюта не установлена.",
                    color=discord.Color.from_rgb(255, 0, 0),
                )
            )
            return
        mute_seconds = None
        try:
            mute_seconds = parse(mute_time)
        # pylint: disable=broad-exception-caught
        except Exception:
            await ctx.respond(
                embed=discord.Embed(
                    title="Неверный формат",
                    description="Формат времени неверен (XhYmZs - X часов Y минут Z секунд)",
                    color=discord.Color.from_rgb(255, 0, 0),
                )
            )
            return
        mutes = self.bot.mutes.get(ctx.guild.id, [])
        try:
            role = discord.utils.get(ctx.guild.roles, id=mute_role_id)
            await user.add_roles(role)
        except Exception:
            await ctx.respond(
                embed=discord.Embed(
                    title="Недостаточно прав",
                    description="У бота недостаточно прав для выдачи мьюта",
                    color=discord.Color.from_rgb(255, 0, 0),
                )
            )
            # pylint: enable=broad-exception-caught`
            return
        mutes.append(
            {
                "user_id": user.id,
                "role_id": mute_role_id,
                "time": mute_seconds.hour * 60 * 60
                + mute_seconds.minute * 60
                + mute_seconds.second,
                "reason": reason,
                "start": datetime.datetime.now().timestamp(),
            }
        )
        self.bot.mutes[ctx.guild.id] = mutes
        self.sync_db(ctx.guild.id)
        await ctx.respond(
            embed=discord.Embed(
                title="Успех!",
                description=f"{user.mention} был успешно замьючен на "
                f"{mute_time} по причине {reason}",
                color=discord.Color.from_rgb(0, 255, 0),
            )
        )
        await asyncio.sleep(mute_seconds.timestamp())
        await user.remove_roles(role)


def setup(bot):
    bot.add_cog(Moderation(bot))
    print("[I] [Moderation] Cog loading!")


# pylint: disable=unused-argument


def teardown(bot):
    print("[I] [Moderation] Cog unloading! Cleaning up...")
    for guild in bot.guilds:
        bot.moderation_cog.sync_db(guild)


# pylint: disable=unused-argument
