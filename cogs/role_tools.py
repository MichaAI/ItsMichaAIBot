import discord
from discord.ext import commands


class RoleTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def give_role(self, ctx,
                        member: discord.Member, role: discord.Role):
        if not (ctx.author.guild_permissions.administrator or
                ctx.author.guild_permissions.manage_roles):
            await ctx.respond(content="У вас нет полномочий на выдачу ролей.")
            return

        if ctx.author.top_role <= role:
            await ctx.respond(
                content=f"Вы не можете выдать роль {role} потому что она"
                "находится выше вашей самой высокой роли.")
            return

        if role in member.roles:
            await ctx.respond(
                content=f"Вы не можете выдать роль {role} "
                "потому что у участника {member.display_name} ({member}) уже есть эта роль.")
            return

        await member.add_roles(role)
        await ctx.respond(content=f"Пользователю {member.display_name} выдана роль {role}.")

    @commands.slash_command()
    async def remove_role(self, ctx, member: discord.Member, role: discord.Role):
        if not (ctx.author.guild_permissions.administrator or
                ctx.author.guild_permissions.manage_roles):
            await ctx.respond(content="У вас нет полномочий на снятие ролей.")
            return

        if ctx.author.top_role <= role:
            await ctx.respond(
                content=f"Вы не можете снять роль {role} потому "
                "что она находится выше вашей самой высокой роли.")
            return

        if role not in member.roles:
            await ctx.respond(
                content=f"Вы не можете снять роль {role} потому что"
                        "у участника {member.display_name} ({member}) отсутствует эта роль.")
            return

        await member.remove_roles(role)
        await ctx.respond(content=f"У пользователя {member.display_name} снята роль {role}.")


def setup(bot):
    bot.add_cog(RoleTools(bot))
