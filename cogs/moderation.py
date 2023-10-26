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
            mute_role = role.id
            server_id = ctx.guild.id
            cursor.execute("SELECT mute_role_id FROM mute_role WHERE server_id = ?", )
            print(cursor.fetchone())






def setup(bot):
    bot.add_cog(moderation(bot))