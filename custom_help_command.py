import discord
from discord.ext import commands


class CustomHelpCommand(commands.HelpCommand):
    def get_command_signature(self, command):
        return (
            f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"
        )

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Команда помощи")
        for cog, bot_commands in mapping.items():
            command_signatures = []
            for c in bot_commands:
                if isinstance(c, discord.ext.commands.Command):
                    if c.aliases:
                        command_signatures.append(
                            f"`{self.context.clean_prefix}{c.qualified_name}`"
                            "{c.signature}"
                        )
                    else:
                        command_signatures.append(
                            f"`{self.context.clean_prefix} {c.qualified_name}`"
                        )
            if command_signatures:
                cog_name = getattr(cog, "qualified_name", None)
                if cog_name:
                    cog_name = cog.qualified_name
                else:
                    cog_name = "Без категории"
                embed.add_field(
                    name=f"{cog_name}:",
                    value="\n\t".join(command_signatures),
                    inline=False,
                )

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_command_help(self, command):
        embed = discord.Embed(title=f"Команда {self.get_command_signature(command)}")
        if command.help:
            embed.description = command.help
        else:
            embed.description = "Нет данных о команде"
        if command.aliases:
            embed.add_field(
                name="Способы вызова:",
                value=f'{command.qualified_name}, {", ".join(command.aliases)}',
                inline=False,
            )

        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(
            title=self.get_command_signature(group), description=group.help
        )

        filtered_commands = await self.filter_commands(group.commands)

        if filtered_commands:
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command), value=command.help
                )

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(
            title=f'{cog.qualified_name or "Без категории"}:',
            description=cog.description,
        )

        filtered_commands = await self.filter_commands(cog.get_commands())

        if filtered_commands:
            for command in filtered_commands:
                embed.add_field(
                    name=self.get_command_signature(command), value=command.help
                )

        await self.get_destination().send(embed=embed)
