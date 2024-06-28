from discord.ext import commands
import discord
import typing
from typing import Literal


######################### --Format-- ############################################################
def discord_print(title="Commands", description="", colour=discord.Color.blurple()):
    embed = discord.Embed(
        title=title,
        description=description,
        color=colour,
    )
    return embed


######################### ---Command Class--- ############################################################
class BasicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ######################### Hello ############################################################
    @commands.command()
    @commands.guild_only()
    async def hello(
        self, ctx: commands.Context, member: typing.Optional[discord.Member] = None
    ):
        if member is None:
            return await ctx.send(f" Hello! {ctx.author.display_name}, How you doing?")

        return await ctx.send(f"{ctx.author.display_name} says hello, {member.mention}")

    ######################### ping ############################################################
    @commands.command()
    @commands.guild_only()
    async def ping(
        self, ctx: commands.Context, member: typing.Optional[discord.Member] = None
    ):
        if member is None:
            return await ctx.send(ctx.author.mention)

        return await ctx.send(member.mention)

    ######################### Ban ############################################################
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def ban(
        self,
        ctx: commands.Context,
        members: commands.Greedy[discord.Member] = None,
        time_number: typing.Optional[int] = 5,
        time_str: Literal["s", "hr", "min", "d"] = None,
        *reason: typing.Optional[str],
    ):
        if not members or time_str is None:
            embed = discord_print(
                "Expected Args:",
                "!ban \n'members' \n'Time' \n[s,hr, min, d]  \n'reason'",
                discord.Color.red(),
            )
            return await ctx.send(embed=embed)

        if not reason:
            reason = "To cute to handle"

        Time_Multipliers = {"d": 86400, "hr": 3600, "min": 60, "s": 1}
        time_in_seconds = time_number * Time_Multipliers.get(time_str, 1)

        ##Banning
        for member in members:
            await member.ban(
                delete_message_seconds=time_in_seconds, reason=" ".join(reason)
            )
            return await ctx.send(
                f"**Banned** *{member.display_name}* \n**Deleted** :  *messages of {time_number}{time_str}* \n**Reason** : *{" ".join(reason)}* "
            )

    ######################### say ############################################################
    @commands.command()
    async def say(self, ctx: commands.Context, *content: str):
        if not content:
            embed = discord_print("Say", "Type something to say", discord.Color.red())
            return await ctx.send(embed=embed)

        return await ctx.send(f"{" ".join(content)},  -*{ctx.author}*")

    ######################### commands ############################################################
    @commands.command()
    async def commands(
        self, ctx: commands.Context, member: typing.Optional[discord.Member] = None
    ):
        list_of_commands = "\n".join([command.name for command in self.bot.commands])
        embed = discord_print("Commands", list_of_commands, discord.Color.blurple())
        return await ctx.send(embed=embed)


######################### -----Setup----- ############################################################
async def setup(bot: commands.Bot):
    await bot.add_cog(BasicCommands(bot))
