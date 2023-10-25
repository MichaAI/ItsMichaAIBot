import discord
from discord.ext import commands
import coreData
import os
SETTINGS = {
    'token': coreData.token,
#    'bot': 'Its MichaAIs bot', # нигде не используются??
#    'id': 1147250594776612948,
    'prefix': '*',
    
    'log_messages': False,
    'owner_id': 629999906429337600,
    'persona_prefix': "Mb:"
}
bot = commands.Bot(command_prefix=commands.when_mentioned_or(SETTINGS['prefix']), intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('bot ready')

@bot.event
async def on_message(message):
    if SETTINGS['log_messages']:
        print(f"Сервер: {message.guild.name} Канал: {message.channel.name} Автор: {message.author.name} Сообщение: {message.content}")
    if message.author == bot.user: return

    await bot.process_commands(message)
    
    #if bot.user.mention in message.content: # зачем засорять консоль?
    #    print(message.author.mention)
    if message.content.startswith(SETTINGS['persona_prefix']) and message.author.id == SETTINGS['owner_id']:
        await message.channel.send(message.content[len(SETTINGS['persona_prefix']):], reference=(message.reference or None))
        await message.delete()

def main():
    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            bot.load_extension("cogs." + f[:-3])

    bot.run(SETTINGS['token'])

if __name__ == "__main__":
    main()
