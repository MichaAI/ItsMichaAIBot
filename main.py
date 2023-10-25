import discord
from discord.ext import commands
import coreData
import os
SETTINGS = {'token': coreData.token, 'bot': 'Its MichaAIs bot', 'id': 1147250594776612948, 'prefix': '*'}
bot = commands.Bot(command_prefix=commands.when_mentioned_or(SETTINGS['prefix']), intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('ready')

@bot.command(aliases=["Привет", "привет"])
async def hi(ctx):
    await ctx.reply(f"Здравствуй, {ctx.message.author.mention}")

@bot.event
async def on_message(message):
    print(f"Сервер: {message.guild.name} Канал: {message.channel.name} Автор: {message.author.name} Сообщение: {message.content}")
    await bot.process_commands(message)
    if message.author != bot.user:
        if bot.user.mention in message.content:
            print(message.author.mention)
        if message.content.startswith("Mb:") and message.author.id == 629999906429337600:
            if message.reference:
                await message.channel.send(message.content[3:], reference=message.reference)
            else:
                await message.channel.send(message.content[3:])
            await message.delete()
    await bot.process_commands(message)

@bot.slash_command(name='тест', description='Что-то делает.', guild_ids=None)
async def test_(ctx):
    await ctx.respond('Успешный тест!')

@bot.slash_command()
@commands.is_owner()
async def reload_cogs(ctx):
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            if "cogs." + f[:-3] in bot.extensions:
                bot.unload_extension("cogs." + f[:-3])
                bot.load_extension("cogs." + f[:-3])
            else:
                bot.load_extension("cogs." + f[:-3])
            await ctx.send("cogs." + f[:-3] + ' reloaded')

def main():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            bot.load_extension("cogs." + f[:-3])

    bot.run(SETTINGS['token'])

if __name__ == "__main__":
    main()