import discord
from discord.ext import commands
import typing
import re
from ..basic.custom_msg import expected_args
from .audio import ytdl_audio


################################################################################################################
###################################### --Music commands class--- ###############################################
###############################################################################################################

"""
class musicCommands

permission : guild only

    join
        !join. (you must be in voice channel first)
    play
        !play song_name
        !play song_url
"""


class musicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

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

    ######################### Play Music ############################################################
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

            FFMPEG_OPTIONS = {
                "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 7",
                "options": "-vn",
            }

            type = "url" if url_pattern.search(song) else "text"
            response = ytdl_audio(song, type)

            ctx.voice_client.play(
                discord.FFmpegPCMAudio(response["url"], **FFMPEG_OPTIONS)
            )
            text = re.sub(re.compile(r"(?<=\b\w) (?=\w\b)"), "", response["title"])

            return await ctx.send(
                f"Now playing:  :notes: **{"".join((text.split("  ")))}**"
            )

        except Exception as e:
            return await ctx.send(f"Error on playing {e}")
