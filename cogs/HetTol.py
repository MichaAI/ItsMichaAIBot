# импортируем необходимые библиотеки
import discord
from discord.ext import commands, tasks
import socket
import select

# создаем класс cog
class PingCog(commands.Cog):
    # инициализируем cog
    def __init__(self, bot):
        self.bot = bot
        # создаем экземпляр сокета
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # привязываем сокет к 3000 порту
        self.s.bind(("", 3000))
        # слушаем входящие соединения
        self.s.listen()
        # запускаем задачу для прослушивания пингов
        self.listen_ping.start()

    # создаем задачу для прослушивания пингов
    @tasks.loop(seconds=1)
    async def listen_ping(self):
        # проверяем, есть ли ожидающие соединения
        ready, _, _ = select.select([self.s], [], [], 0)
        # если есть, то принимаем их
        if ready:
            # принимаем соединение
            conn, addr = self.s.accept()
            # получаем данные
            data = conn.recv(1024)
            # отправляем ответ "pong"
            conn.send(b"pong")
            # закрываем соединение
            conn.close()

    # останавливаем задачу при выгрузке cog
    # закрываем сокет при выгрузке cog
    def cog_unload(self):
            self.listen_ping.cancel()
            self.s.close()

# добавляем cog к боту
def setup(bot):
    bot.add_cog(PingCog(bot))

