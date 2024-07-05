import os
import dotenv
import discord
from discord.ext import commands
import asyncio

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")


async def main():
    assert TOKEN, "TOKEN NOT PROVIDED"

    bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
    await bot.load_extension("cogs.basic")
    await bot.load_extension("cogs.listener")
    await bot.load_extension("cogs.channel")
    await bot.load_extension("cogs.musicplayer")

    return await bot.start(TOKEN)


asyncio.run(main())
