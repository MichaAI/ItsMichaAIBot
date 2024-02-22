import random
import discord
from discord.ext import commands

with open("./commands/rm.txt") as file:
    rm_help = file.read()

phrases = [
    "Опять эта банда творит шизу...",
    "Аа... у нас тут есть некоторые люди, которые часто несут чушь.",
    "Но это не шутка... тут нет ничего от шутки.",
    "Ах-ох...",
    "Ну только не опять...",
    "Боже...",
    "Господи.",
    "Я не думаю, что это стоило писать сюда.",
    "Ща в мут отлетишь за странное поведение и капс.",
    "*тихое проявление недовольства*",
    "С меня уже хватит.",
    "Не хочу опять заходить в чат и обнаруживать, какой ужас в этот раз происходит здесь.",
    "Надоели мне твои выходки, у меня аж настроение испортилось.",
    "Вот и настроение пропало.",
    "Настроение паршивое вновь.",
    "Боже мой, хватит уже.",
    "Спасибо за испорченное на весь день настроение. ",
    "Настроение испорчено...",
    "Мне кажется, или это точно не нужно кидать в этот канал...",
    "А это тут при чём...",
    "А так... зачем это вообще...",
    "Можешь проверить все мои сообщения на сервере, если настолько делать нечего.",
    "Ну как обычно, нельзя нормально воспринять, нужно высмеять тут же. <:felms1:1205510982923980831>",
    "Что во мне такого особенного?... Я просто... испортился со временем <:blossombud_ugh:1146385811026214942> Проблем от меня уже больше, чем пользы... Порчу всем настроение своим присутствием..",
    "Моя психика уже рушится и я не могу воспринимать текстовый юмор практически ни в каком виде. <:felms1:1205510982923980831>",
    "Убедительная просьба прекратить спам упоминаниями. Заранее спасибо за понимание.",
    "Не споткнись по дороге 👋",
    "Вот это ты зря быканул. Такой наглости я не ожидал от вашей персоны.",
]


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["Привет", "привет"])
    async def hi(self, ctx):
        await ctx.reply(f"Здравствуй, {ctx.message.author.mention}!")

    @commands.command(aliases=["bаn", "бaн"])
    async def banan(self, ctx, *, reason: str = "None"):
        if not ctx.message.reference:
            return
        original = await ctx.fetch_message(ctx.message.reference.message_id)
        await ctx.reply(
            f"Пользователь {original.author.mention} был забанен пользователем {ctx.message.author.mention} по причине `{reason}`"
        )

    @commands.command(aliases=["взорвался"])
    async def explode(self, ctx: discord.ApplicationContext):
        msg = []
        async for message in ctx.channel.history(limit=100):
            if message.author == ctx.message.author:
                continue
            if message.author in msg:
                continue
            msg.append(message.author)
        parts = [
            "прилетела голова",
            "прилетела правая рука",
            "прилетела левая рука",
            "прилетела правая нога",
            "прилетела левая нога",
            "прилетело туловище",
            "прилетело сердце",
            "прилетели глаза",
            "прилетел мозг",
            "прилетел язык",
            "прилетела печень",
            "прилетел желудок",
            "прилетели лёгкие",
        ]
        msg = msg[: len(parts) - 1]
        exploded = ""
        for i in range(random.randint(2, 10)):
            safety_limit = 100
            _ = 0
            while _ < safety_limit:
                part = random.choice(parts)
                _ += 1
                if part in exploded:
                    continue
                exploded += f"**В {random.choice(msg).mention} {part}**\n"
                break
        await ctx.reply(
            f"**{ctx.message.author.mention} взорвался!**\n" + exploded.strip(),
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @commands.command(aliases=["фраза-фелмса"])
    async def mood(self, ctx):
        await ctx.reply(random.choice(phrases))

    @commands.Cog.listener()
    async def on_message(self, message):
        if random.randint(1, 200) != 200:
            return
        await message.channel.send(random.choice(phrases), delete_after=30)

    @commands.command(aliases=["rm"])
    async def mood(self, ctx, flags: str = None, directory: str = None):
        if not flags and not directory:
            await ctx.reply(
                "rm: missing operand \n" "Try 'rm --help' for more information."
            )
            return

        if flags == "--help":
            await ctx.reply(rm_help)
            return

        if not flags.startswith("-"):
            if not directory:
                await ctx.reply(
                    f"Файл {flags} не найденн, файл {directory} успешно удаленн"
                )
                return
            await ctx.reply(f"Директория {flags} не найденна")

        if flags == "-rf" and directory == "/*":
            await ctx.reply("Система успешно удаленна! Удачного дня!")
            return

        if "r" in flags:
            await ctx.reply(f"Директория {directory} успешно удаленна!")
            return

        await ctx.reply(f"Файл {directory} успешно удаленн!")


def setup(bot):
    bot.add_cog(Fun(bot))
