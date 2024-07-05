from discord.ext import commands
import discord
import typing
# import re

from ..basic.custom_msg import expected_args
# from ..musicplayer.audio import ytdl_audio


"""
class Channel

<permission : manage_guild = True>
    newcategory
    newchannel
    delchannel
    delcategory

"""


class Channel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ######################### Create category ############################################################
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def newcategory(self, ctx: commands.Context, name: str = None):
        """
        Creates a new category in the server.

        Example:
            !newcategory 'text only'

        Arguments:
            name (str): The name of the category to be created.
                        If not provided, an error message will be shown.

        Raises:
            discord.DiscordException: If an error occurs while creating the category.
        """
        try:
            if name is None:
                return await ctx.send(
                    embed=expected_args(
                        "!newcategory\n*name of category*", discord.Color.red()
                    )
                )
            await ctx.guild.create_category(name=name)
            return await ctx.send(f"New category created: **{name}**")
        except Exception as e:
            await ctx.send(f"An error occurred while creating the category: {e}")

    ######################### Create new Channel ############################################################
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def newchannel(
        self,
        ctx: commands.Context,
        type: typing.Optional[str] = None,
        name: str = None,
        *,
        category: typing.Optional[str] = None,
    ):
        try:
            if name is None or type not in ["t", "text", "v", "voice"]:
                return await ctx.send(
                    embed=expected_args(
                        "!newchannel \n*type[voice =  v, text = t]* \n*name*",
                        discord.Color.red(),
                    )
                )

            if category is None:
                category = ctx.channel.category
            else:
                for each in ctx.guild.categories:
                    if (each.name).lower() == category.lower():
                        category = each
                        break

            type = "voice" if type in ["v", "voice"] else "text"

            if type == "text":
                await ctx.guild.create_text_channel(name=name, category=category)
            else:
                await ctx.guild.create_voice_channel(name=name, category=category)

            return await ctx.send(
                f"New {type} channel created : **{name}** in {category}"
            )

        except Exception as e:
            await ctx.send(f"Cannot create channel {e}")

    ######################### Delete Channel ############################################################
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def delchannel(
        self,
        ctx: commands.Context,
        channels: commands.Greedy[
            typing.Union[discord.TextChannel, discord.VoiceChannel]
        ] = None,
    ):
        try:
            if channels is None:
                return await ctx.send(
                    embed=expected_args(
                        "!delchannel\n *channel*",
                        discord.Color.red(),
                    )
                )

            list_channel = []
            for channel in channels:
                list_channel.append(channel.name)
                await channel.delete()
            return await ctx.send(f"Deleted Channel :  **{" ".join(list_channel)}**")

        except Exception as e:
            await ctx.send(f"Error on Deleting your request {e}")

    ######################### Delete Category ############################################################
    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    async def delcategory(
        self, ctx: commands.Context, category: discord.CategoryChannel = None
    ):
        try:
            if category is None:
                return await ctx.send(
                    embed=expected_args(
                        "!delcategory \n*category*",
                        discord.Color.red(),
                    )
                )
            await category.delete()
            return await ctx.send(f"Deleted Category **{category}**")
        except Exception as e:
            await ctx.send(f"Cannot delete category {e}")


######################### Setup ##################################################################
async def setup(bot: commands.Bot):
    await bot.add_cog(Channel(bot))
