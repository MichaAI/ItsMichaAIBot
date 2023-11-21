import discord
from discord.ext import commands

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel == after.channel:
            return #скрипт закончится если канал не изменился
        # здесь должно быть обращение к бд
        if after.channel is not None: # здесь нужно сделать что бы если канал есть в бд код не исполнялся
            role_name = after.channel.name
            role = discord.utils.get(member.guild.roles, name=role_name)
            if role is None: #если роли нету на сервере
                await member.guild.create_role(name=role_name, mentionable=True) #coздаем ее
            await member.add_roles(role) #добавляем роль пользователю
        if before.channel is not None:
            role_name = before.channel.name
            role = discord.utils.get(member.guild.roles, name=role_name)
            if role is None:
                return #если такой роли нету, ничего убирать и не придется
            await member.remove_roles(role)

    @commands.slash_command()
    async def ignore_voice_channel(self, ctx, role: discord.VoiceChannel):
        await ctx.respond("здесь нужно <@891289716501119016> сделать что бы указанный канал не создавал роли для упоминания учасников этого канала")


def setup(bot):
    bot.add_cog(voice(bot))
