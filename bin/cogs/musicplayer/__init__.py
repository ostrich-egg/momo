from discord.ext import commands

# from . import musicCommands
from .musicCommands import musicCommands


######################### Setup ##################################################################
async def setup(bot: commands.Bot):
    await bot.add_cog(musicCommands(bot))
