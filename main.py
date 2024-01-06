import discord
from discord.ext import commands
import os
import signal
import atexit
import pymongo
from Custom_Help_Command import CustomHelpCommand

SETTINGS = {
    'token': None,
    'bot': 'Its MichaAIs bot',  # нигде не используются??
    'id': 1147250594776612948,
    'prefix': '*',

    'log_messages': False,
    'owner_id': 629999906429337600,
    'persona_prefix': "Mb:",

    'mongo': {
        'prefix': 'mongodb://',
        'host': 'localhost',
        'port': '27017',
    },
}

try:
    with open("./token.txt", 'r') as f:
        SETTINGS['token'] = f.readlines()[0]
except Exception as e:
    print(f"ERROR! Failed to read tokenfile: {e}")
    exit(1)

client = pymongo.MongoClient(SETTINGS['mongo']['prefix'] + SETTINGS['mongo']['host'] + ":" + SETTINGS['mongo']['port'])

bot = commands.Bot(command_prefix=commands.when_mentioned_or(SETTINGS['prefix']), intents=discord.Intents.all())


@bot.event
async def on_ready():
    print('bot ready')


@bot.event
async def on_message(message):
    if message.author.id == 891289716501119016
        await message.delete() #если пытаешься бвть злым, пытайся лучше...
    if SETTINGS['log_messages']:
        print(f"Сервер: {message.guild.name} Канал: {message.channel.name} Автор:"
              f" {message.author.name} Сообщение: {message.content}")
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    if message.content.startswith(SETTINGS['persona_prefix']) and message.author.id == SETTINGS['owner_id']:
        await message.channel.send(message.content[len(SETTINGS['persona_prefix']):],
                                   reference=(message.reference or None))
        await message.delete()


@bot.slash_command()
@commands.is_owner()
async def reload_cogs(ctx):
    print("[I] Cogs reload requested!")
    embed = discord.Embed(title="Reloading cogs...")
    load_suc = 0
    load_err = 0
    for f in os.listdir("./cogs"):
        if not f.endswith(".py"):
            continue
        if "cogs." + f[:-3] in bot.extensions:
            try:
                bot.unload_extension(f"cogs.{f[:-3]}")
                bot.load_extension(f"cogs.{f[:-3]}")
                embed.add_field(name=f"cog {f[:-3]} (OK)", value="Successfully reloaded", inline=False)
                print(f"[I] Cog {f[:-3]} reloaded")
            except Exception as e:
                load_err += 1
                embed.add_field(name=f"cog {f[:-3]} (FAIL)", value=f"{e}")
                print(f"[E] ERROR! Cog {f[:-3]} reloading failed: {e}")
            else:
                load_suc += 1
        else:
            try:
                bot.load_extension(f"cogs.{f[:-3]}")
                embed.add_field(name=f"cog {f[:-3]} (OK)", value="Successfully loaded", inline=False)
                print(f"[I] Cog {f[:-3]} loaded")
            except Exception as e:
                load_err += 1
                embed.add_field(name=f"cog {f[:-3]} (FAIL)", value=f"{e}")
                print(f"[E] ERROR! Cog {f[:-3]} loading failed: {e}")
            else:
                load_suc += 1

    if load_suc == load_suc + load_err:
        embed.set_footer(text=f"All cogs ({load_suc}) were reloaded successfully")
    elif load_err == load_suc + load_err:
        embed.set_footer(text=f"ERROR!!! All cogs ({load_err}) was failed to reload! Call gary!!!")
    else:
        embed.set_footer(text=f"Cogs (re)loaded: {load_suc}/{load_suc + load_err} "
                              f"| Cogs errored: {load_err}/{load_suc + load_err}")

    await ctx.respond(embed=embed, ephemeral=False)


def main():
    bot.help_command = CustomHelpCommand(
        command_attrs={'name': "help", 'aliases': ["helpme", "помощь", "хелп"]})
    bot.dbclient = client

    for f in os.listdir("./cogs"):
        if not f.endswith(".py"):
            continue
        try:
            bot.load_extension("cogs." + f[:-3])
            print(f"[I] Cog {f[:-3]} loaded")
        except Exception as e:
            print(f"[E] ERROR! Cog {f[:-3]} loading failed: {e}")

    bot.run(SETTINGS['token'])
    handle_exit()


def handle_exit(*args):
    print("[I] EXIT signal received!\n[I] Proceeding with cleanup")
    for f in os.listdir("./cogs"):
        if not f.endswith(".py"):
            continue
        try:
            bot.unload_extension("cogs." + f[:-3])
            print(f"[I] Cog {f[:-3]} unloaded.")
        except Exception as e:
            print(f"[E] ERROR! Cog {f[:-3]} unloading failed: {e}")


if __name__ == "__main__":
    main()

atexit.register(handle_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)
