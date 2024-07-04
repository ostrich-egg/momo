from discord.ext import commands
import discord
import typing
import re

from ..basic.custom_msg import expected_args
from .audio import ytdl_audio


"""
class Channel

<permission : manage_guild = True>
    newcategory
    newchannel
    delchannel
    delcategory
    join
    play

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

    ######################### Join Voice Channel ############################################################
    @commands.command()
    @commands.guild_only()
    async def join(
        self,
        ctx: commands.Context,
    ):
        try:
            if not ctx.author.voice:
                return await ctx.send("You are not in voice channel")

            channel = ctx.author.voice.channel

            if ctx.voice_client:
                await ctx.voice_client.disconnect()

            await channel.connect()
            # ffopts = {"options": "-vn"}
            # ctx.voice_client.play(discord.FFmpegPCMAudio(extract_audio()))
            return await ctx.send(f"Joined channel **{channel}**")

        except Exception as e:
            return await ctx.send(f"Cannot join. {e}")

        ######################### Join Voice Channel ############################################################

    @commands.command()
    @commands.guild_only()
    async def play(
        self,
        ctx: commands.Context,
        *,
        song=None,
    ):
        try:
            if ctx.voice_client is None:
                return await ctx.send("Allow me to join voice channel first")

            if song is None:
                return await ctx.send(embed=expected_args("!play \n*[title or url]*"))

            url_pattern = re.compile(
                r"^(https?://)?(www\.)?"
                r"(youtube|youtu|youtube-nocookie)\.(com|be)/"
                r"(watch\?v=|embed/|v/|.+\?v=|.+/)?([^&=%\?]{11})"
            )
            type = "url" if url_pattern.search(song) else "text"
            response = ytdl_audio(song, type)

            ctx.voice_client.play(discord.FFmpegPCMAudio(response["url"]))
            text = re.sub(re.compile(r"(?<=\b\w) (?=\w\b)"), "", response["title"])

            return await ctx.send(f"Now playing:  **{"".join((text.split("  ")))}**")

        except Exception as e:
            return await ctx.send(f"Error on playing {e}")


######################### Setup ##################################################################
async def setup(bot: commands.Bot):
    await bot.add_cog(Channel(bot))
