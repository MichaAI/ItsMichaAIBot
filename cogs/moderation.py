import discord
import asyncio
from discord.ext import commands
import pymongo
import datetime

def parse(s):
    fmt=''.join('%'+c.upper()+c for c in 'hms' if c in s)
    return datetime.datetime.strptime(s, fmt).time()

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.mutes = {}
        self.bot.moderation_cog = self
        self.db_client = self.bot.dbclient

        def _unmute_after(bot, mute):
            role = discord.utils.get(guild.roles, id=mute['role_id'])
            user = discord.utils.get(guild.members, id=mute['user_id'])

            await asyncio.sleep((mute['start'] + mute['time']) - datetime.datetime.now().timestamp())
            await user.remove_roles(role)
            
        for guild in bot.guilds:
            mutes = list(self.db_client.mutes.data.find({'guild_id': guild.id}))
            if len(mutes) == 0:
                self.db_client.mutes.data.insert_one({'guild_id': guild.id})
                mutes = self.db_client.mutes.data.find({'guild_id': guild.id})
            bot.mutes[guild.id] = mutes[0]
            for mute in bot.mutes[guild.id]:
                if mute['start'] + mute['time'] < datetime.datetime.now().timestamp():
                    role = discord.utils.get(guild.roles, id=mute['role_id'])
                    user = discord.utils.get(guild.members, id=mute['user_id'])
                    await user.remove_roles(role)
                    continue
                asyncio.create_task(_unmute_after(bot, mute))
                    

    def sync_db(self, target_guild_id):
        mutes = list(self.db_client.mutes.data.find({'guild_id': target_guild_id}))
        if len(mutes) == 0:
            self.db_client.mutes.data.insert_one({'guild_id': target_guild_id})
            mutes = self.db_client.mutes.data.find({'guild_id': target_guild_id})
        mutes = mutes[0]
        self.db_client.mutes.data.update_one({'guild_id': target_guild_id}, {'$set': {'role_id': bot.mutes.get(target_guild_id, {})}})

    @commands.slash_command()
    async def set_mute_role(self, ctx, role: discord.Role):
        if not ctx.author.guild_permissions.administrator:
            await ctx.respond(embed=discord.Embed(title="Недостаточно полномочий.",
                              description=f"Вам не хватает прав для исполнения команды.",
                              color=discord.Color.from_rgb(255, 0, 0)))
            return
        mute_role_id = role.id
        server_id = ctx.guild.id
        mutes_config = list(self.db_client.mutes.config.find({'guild_id': server_id}))
        if len(mutes_config) == 0:
            self.db_client.mutes.config.insert_one(
                {
                    'guild_id': server_id,
                    'role_id': -1
                }
            )
            mutes_config = self.db_client.mutes.config.find({'guild_id': server_id})
        mutes_config = mutes_config[0]
        if mutes_config['role_id'] == mute_role_id:
            await ctx.respond(embed=discord.Embed(title="Равное значение.",
                              description=f"Установленная роль мьюта равна данной.",
                              color=discord.Color.from_rgb(255, 0, 0)))
            return
        self.db_client.mutes.config.update_one({'guild_id': server_id}, {'$set': {'role_id': mute_role_id}})
        await ctx.respond(embed=discord.Embed(title="Успех!",
                          description=f"Роль мьюта установлена.",
                          color=discord.Color.from_rgb(0, 255, 0)))

    @commands.slash_command()
    async def mute(self, ctx, user: discord.Member, mute_time: str="12h0m0s", reason: str="Не указана"):
        if not (ctx.author.guild_permissions.mute_members or ctx.author.guild_permissions.administrator):
            await ctx.respond(embed=discord.Embed(title="Недостаточно полномочий",
                              description=f"Вам не хватает прав для исполнения команды.",
                              color=discord.Color.from_rgb(255, 0, 0)))
            return
        server_id = ctx.guild.id
        mutes_config = list(self.db_client.mutes.config.find({'guild_id': server_id}))
        if len(mutes_config) == 0:
            self.db_client.mutes.config.insert_one(
                {
                    'guild_id': server_id,
                    'role_id': -1
                }
            )
            mutes_config = self.db_client.mutes.config.find({'guild_id': server_id})
        mutes_config = mutes_config[0]
        mute_role_id = mutes_config['role_id']
        if mute_role_id == -1:
            await ctx.respond(embed=discord.Embed(title="Неверная конфигурация",
                              description=f"Роль мьюта не установлена.",
                              color=discord.Color.from_rgb(255, 0, 0)))
            return
        mute_seconds = datetime.time(0)
        try:
            mute_seconds = hms(mute_time)
        finally:
            if mute_seconds == datetime.time(0):
                await ctx.respond(embed=discord.Embed(title="Неверный формат",
                                  description=f"Формат времени неверен (XhYmZs - X часов Y минут Z секунд)",
                                  color=discord.Color.from_rgb(255, 0, 0)))
                return
        mutes = bot.mutes.get(ctx.guild.id, [])
        try:
            role = discord.utils.get(ctx.guild.roles, id=mute_role_id)
            await user.add_roles(role)
        except:
            await ctx.respond(embed=discord.Embed(title="Недостаточно прав",
                              description=f"У бота недостаточно прав для выдачи мьюта",
                              color=discord.Color.from_rgb(255, 0, 0)))
                return
        mutes.append({
            'user_id': user.id,
            'role_id': mute_role_id,
            'time': mute_seconds.timestamp(),
            'reason': reason,
            'start': datetime.datetime.now().timestamp()
        })
        bot.mutes[ctx.guild.id] = mutes
        self.sync_db(ctx.guild.id)
        await ctx.respond(embed=discord.Embed(title="Успех!",
                          description=f"{user.mention} был успешно замьючен на {mute_time} по причине {reason}",
                          color=discord.Color.from_rgb(0, 255, 0)))
        await asyncio.sleep(mute_seconds.timestamp())
        await user.remove_roles(role)





def setup(bot):
    bot.add_cog(moderation(bot))
    print('[I] [Moderation] Cog loading!')

def teardown(bot):
    print('[I] [Moderation] Cog unloading! Cleaning up...')
    for guild in bot.guilds:
        bot.moderation_cog.sync_db(guild)
