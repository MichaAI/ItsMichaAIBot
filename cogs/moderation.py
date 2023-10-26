import discord
import asyncio
from discord.ext import commands
import sqlite3

conn = sqlite3.connect('../database.db')  # Подключение к базе данных
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS mute_role (id INTEGRER PRIMARY KEY, server_id INTEGRER, mute_role_id INTEGRER)")
cursor.execute("CREATE TABLE IF NOT EXISTS mute (id INTEGER PRIMARY KEY, server_id INTEGER, mute_role_id INTEGER, member_id INTEGER, end_time INTEGER)")

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mute_tasks = {}

    @commands.slash_command()
    async def set_mute_role(self, ctx, role: discord.Role):
        if ctx.author.guild_permissions.administrator:
            mute_role_id = role.id
            server_id = ctx.guild.id
            cursor.execute("SELECT mute_role_id FROM mute_role WHERE server_id = ?", (server_id,))
            mute_role = cursor.fetchall()
            newrole = discord.utils.get(ctx.guild.roles, id=int(str(mute_role[0])[1:20]))
            if newrole == role:
                await ctx.respond(f"Роль {role} уже установленна в качестве роли мьюта")
            else:
                cursor.execute("INSERT OR REPLACE INTO mute_role (server_id, mute_role_id) VALUES (?, ?)",
                               (server_id, mute_role_id))
                conn.commit()
                await ctx.respond(f"Роль мьюта установленна на {role}")
        else:
            await ctx.respond("Недостаточно полномочий")

    @commands.slash_command()
    async def mute(self, ctx, user: discord.Member, time: int, reson: str):
        if ctx.author.guild_permissions.mute_members or ctx.author.guild_permissions.administrator:
            await ctx.respond("[eq ,j,hf")
        else:
            await ctx.respond(embed = discord.Embed(title="Недостаточно полномочий",
                                              description=f"Вам не хватает прав для исполнения комманды{commands.Context}"))





def setup(bot):
    bot.add_cog(moderation(bot))