import discord
import asyncio
from discord.ext import commands
import pymongo

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_client = self.bot.dbclient
        self.mute_tasks = {}

    @commands.slash_command()
    async def set_mute_role(self, ctx, role: discord.Role):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond(embed=discord.Embed(title="Недостаточно полномочий.",
                              description=f"Вам не хватает прав для исполнения команды.",
                              color=discord.Color.from_rgb(255, 0, 0)))
            return
        mute_role_id = role.id
        server_id = ctx.guild.id
        mutes_config = self.db_client.config.mutes.find({'guild_id': server_id})
        if len(mutes_config) == 0:
            self.db_client.config.mutes.insert_one(
                {
                    'guild_id': server_id,
                    'role_id': -1
                }
            )
            mutes_config = self.db_client.config.mutes.find({'guild_id': server_id})
        if mutes_config['role_id'] == mute_role_id:
            await ctx.respond(embed=discord.Embed(title="Равное значение.",
                              description=f"Установленная роль мьюта равна данной.",
                              color=discord.Color.from_rgb(255, 0, 0)))
            return
        self.db_client.config.mutes.update_one({'guild_id': server_id}, {'$set': {'role_id': mute_role_id}})
        await ctx.respond(embed=discord.Embed(title="Успех!",
                          description=f"Роль мьюта установлена",
                          color=discord.Color.from_rgb(0, 255, 0)))

    @commands.slash_command()
    async def mute(self, ctx, user: discord.Member, time: int, reson: str):
        if not (ctx.author.guild_permissions.mute_members or ctx.author.guild_permissions.administrator):
            await ctx.respond(embed=discord.Embed(title="Недостаточно полномочий",
                              description=f"Вам не хватает прав для исполнения команды{commands.Context}"))
            return
        await ctx.respond("//TODO")





def setup(bot):
    bot.add_cog(moderation(bot))
