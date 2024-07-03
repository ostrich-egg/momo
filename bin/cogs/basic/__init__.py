from discord.ext import commands
import discord
import typing
from typing import Literal

from .custom_msg import discord_print, expected_args

"""
class BasicCommands

    hello
        !hello (it will greet to author)
        !hello @somebody


    ping
        !ping (it will ping to author)
        !ping somebody

    ban
        !ban somebody
        !ban somebody1 somebody2

    unban
        !unban somebody

    kick
        !kick somebody
        !kick somebody1 somebody2

    say
        !say i love you

    roles
        !roles (it will list your roles)
        !roles somebody

    list_role
        !list_role  (it will list role of your guild)

    commands
        !commands
"""


##########################################################################################################
###################################### ---Command Class--- ###############################################
##########################################################################################################


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
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def ban(
        self,
        ctx: commands.Context,
        members: commands.Greedy[discord.Member] = None,
        time_number: typing.Optional[int] = 1,
        time_str: typing.Optional[Literal["s", "hr", "min", "d"]] = "min",
        *reason: typing.Optional[str],
    ):
        if members is None:
            return await ctx.send(
                embed=expected_args(
                    "!ban \n'members' \n'Time' \n[s,hr, min, d]  \n'reason'",
                    discord.Color.red(),
                )
            )

        reason = " ".join(reason) if reason else "To cute to handle"

        Time_Multipliers = {"d": 86400, "hr": 3600, "min": 60, "s": 1}
        time_in_seconds = time_number * Time_Multipliers.get(time_str, 1)

        ##Banning
        for member in members:
            await member.ban(
                delete_message_seconds=time_in_seconds, reason="No Particular Reason"
            )
            return await ctx.send(
                f"**Banned** *{member.display_name}* \n**Deleted** :  *messages of {time_number}{time_str}* \n**Reason** : *{reason}* "
            )

    ######################### unban ############################################################
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_guild_permissions(ban_members=True)
    @commands.has_guild_permissions(ban_members=True)
    async def unban(
        self,
        ctx: commands.Context,
        member: str = None,
        *reason: typing.Optional[str],
    ):
        if member is None:
            return await ctx.send(
                embed=expected_args("*User_name*", discord.Color.red())
            )

        reason = " ".join(reason) if reason else "Mistake on previous ban"

        try:
            ban_list = [ban async for ban in ctx.guild.bans()]

            ban_snowflake = None
            for each in ban_list:
                if each.user.global_name == member:
                    ban_snowflake = each
                    break

            if ban_snowflake is not None:
                await ctx.guild.unban(user=ban_snowflake.user, reason=reason)
                return await ctx.send(
                    f"**Unbanned**: *{member}* \n**Reason**: *{reason}*"
                )
            else:
                embed = discord_print(
                    "Bad Request", "User is not in ban list", discord.Color.red()
                )
                await ctx.send(embed=embed)

        except discord.Forbidden:
            await ctx.send(
                embed=discord_print(
                    "Forbidden",
                    "I currently do not have permissionn",
                    discord.Color.red(),
                )
            )

        except discord.HTTPException as e:
            await ctx.send(
                embed=discord_print(
                    "HTTP",
                    f"Failed to fetch list of ban member: {e}",
                    discord.Color.red(),
                )
            )

    ######################### Kick ############################################################
    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(
        self,
        ctx: commands.Context,
        members: commands.Greedy[discord.Member] = None,
        *reason: typing.Optional[str],
    ):
        if members is None:
            return await ctx.send(
                embed=expected_args(
                    "!kick \n'members(guild's member)' \n'reason(optional)'",
                    discord.Color.red(),
                )
            )
        reason = "No particular reason" if not reason else " ".join(reason)

        for member in members:
            await member.kick(reason=reason)
            return await ctx.send(
                f"**Kicked** *{member.display_name}* \n**Reason** : *{reason}* "
            )

    ######################### say ############################################################
    @commands.command()
    async def say(self, ctx: commands.Context, *content: str):
        if not content:
            return await ctx.send(
                embed=discord_print("Say", "Type something to say", discord.Color.red())
            )

        return await ctx.send(f"{" ".join(content)},  -*{ctx.author}*")

    ######################### Role ############################################################
    @commands.command()
    @commands.guild_only()
    async def roles(self, ctx: commands.Context, member: discord.Member = None):
        member = member if member is not None else ctx.author
        Desc = (
            f"Roles of {member.global_name}"
            if hasattr(member, "global_name") and member.global_name is not None
            else f"Roles of {member.name}"
        )
        roles = [role.name for role in member.roles]
        return await ctx.send(embed=discord_print(f"{Desc} : ", "\n".join(roles)))

    ######################### List roles of guild ############################################################
    @commands.command()
    @commands.guild_only()
    async def list_roles(
        self,
        ctx: commands.Context,
    ):
        guild = ctx.guild
        roles = set(role.name for role in guild.roles)
        return await ctx.send(embed=discord_print("Roles Available", "\n".join(roles)))

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
