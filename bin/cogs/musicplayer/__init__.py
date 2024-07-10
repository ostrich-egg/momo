from discord.ext import commands

from .musicCommands import musicCommands


async def setup(bot: commands.Bot):
    await bot.add_cog(musicCommands(bot))
