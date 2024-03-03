import traceback

import aiohttp
import discord
from discord.ext import commands
from redis import asyncio as aioredis

r = aioredis.StrictRedis(host="localhost", port=6379, decode_responses=True)


def parse(string):
    flags = [""]
    args = [""]
    flag = False
    one_letter_flag = False
    for ch in string:
        if ch == "-":
            if flag and one_letter_flag:
                one_letter_flag = False
                continue
            if flag and not one_letter_flag:
                flags[-1] += "-"
                continue
            flag = True
            one_letter_flag = True
            continue
        if ch == " ":
            if flag:
                flags.append("")
            else:
                args.append("")
            flag = False
            one_letter_flag = False
        if flag and not one_letter_flag:
            flags[-1] += ch
        elif flag:
            flags[-1] += ch
            flags.append("")
        else:
            args[-1] += ch
    return [i.strip() for i in flags], [i.strip() for i in args]


def smartsplit(string):
    parts = [""]
    instr = False
    for ch in string.strip():
        if ch == '"':
            instr = not instr
            continue
        if instr:
            parts[-1] += ch
            continue
        if ch == " ":
            parts.append("")
            continue
    return parts


def parse_cmdline(cmdline):
    commandline = smartsplit(cmdline)
    command = commandline[0]
    return command, *parse(" ".join(commandline[1:]))


async def read_user_env(uid):
    default_env = f"/home/{uid}\xff0\xff/home/{uid}"
    env = await r.get(f"user_{uid}_env")
    if not env:
        await r.set(f"user_{uid}_env", default_env, 3600)
        return await read_user_env(uid)
    env_l = env.split("\xff")
    env = {"CWD": env_l[0], "?": int(env_l[1]), "HOME": env_l[2]}
    return env


async def write_user_env(uid, env):
    env_s = f"{env['CWD']}\xff{env['?']}\xff{env['HOME']}"
    await r.set(f"user_{uid}_env", env_s, 3600)


def form_fs_path(path):
    formed_path = []
    for n, i in enumerate(path.split("/")):
        if i == "":
            continue
        elif i == ".":
            continue
        elif i == "..":
            formed_path = formed_path[:-1]
        else:
            formed_path.append(i)
    return "/" + "/".join(formed_path)


async def pwd_runner(to_globals, env, flags, args):
    for glob in to_globals:
        globals()[glob] = to_globals[glob]

    if "help" in flags:
        print(
            "pwd: pwd\n"
            "    Print the name of the current working directory.\n\n"
            "    Exit Status:\n"
            "    Returns 0 unless an invalid option is given or the current working directory\n"
            "    cannot be read."
        )
        return 0
    elif flags == []:
        pass
    else:
        print(f"msh: pwd: -{flags[0]}: invalid option\n" "pwd: usage: pwd")
        return 2

    print(env["CWD"])
    return 0


async def cd_runner(to_globals, env, flags, args):
    for glob in to_globals:
        globals()[glob] = to_globals[glob]

    if "help" in flags:
        print(
            "cd: cd [dir]\n"
            "    Change the shell working directory\n\n"
            "    Change the current directory to DIR.  The default DIR is the value of the\n"
            "    HOME shell variable.\n\n"
            "    Exit Status:\n"
            "    Returns 0 if the directory is changed, non-zero otherwize."
        )
        return 0
    elif flags == []:
        pass
    else:
        print(f"msh: cd: -{flags[0]}: invalid option\n" "cd: usage: cd [dir]")
        return 2
    if len(args) > 1:
        print(f"msh: cd: -{flags[0]}: too many arguments\n" "cd: usage: cd [dir]")
        return 1
    if args[0].startswith("/"):
        env["CWD"] = form_fs_path(args[0])
        return 0
    env["CWD"] = form_fs_path(env["CWD"] + args[0])
    return 0


async def exec(ctx, cmdline):
    cmd, flags, args = parse_cmdline(cmdline)
    toprint = ""

    def _print(*txt):
        toprint += " ".join(txt) + "\n"

    to_globals = {"print": _print}

    env = await read_user_env(ctx.message.author.id)

    rcode = 1

    if cmd == "pwd":
        rcode = await pwd_runner(to_globals, env, flags, args)
    elif cmd == "cd":
        rcode = await cd_runner(to_globals, env, flags, args)
    else:
        await ctx.reply(f"msh: command not found: {cmd}")
    if rcode is None:
        print(
            f"Command {cmd} returned no return code. THIS IS UNACCEPTABLE! Assuming rcode = 1"
        )
        rcode = 1
    env["?"] = int(rcode)
    await write_user_env(ctx.message.author.id, env)
    await ctx.reply(toprint if toprint else "** **")
    return env["?"]


class Linux(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pwd(self, ctx: commands.Context, *, cmdline: str = ""):
        try:
            exitc = await exec(ctx, f"pwd {cmdline}")
        except BaseException as e:
            nl = "\n"
            await ctx.reply(
                f"{e}\n```{nl.join(traceback.format_exception(type(e), e, e.__traceback__))}\n```"
            )

    @commands.command()
    async def cd(self, ctx: commands.Context, *, cmdline: str = ""):
        exitc = await exec(ctx, f"pwd {cmdline}")

    @commands.command()
    async def ls(self, ctx: commands.Context, *, cmdline: str = ""):
        exitc = await exec(ctx, f"ls {cmdline}")

    @commands.command()
    async def echo(self, ctx: commands.Context, *, cmdline: str = ""):
        await ctx.reply(
            cmdline if cmdline else "** **",
            allowed_mentions=discord.AllowedMentions.none(),
        )

    @commands.command()
    async def curl(self, ctx: commands.Context, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                await ctx.reply(f"Status: {response.status} \n\n"

                                f"Json: {await response.json()}")



def setup(bot):
    bot.add_cog(Linux(bot))
