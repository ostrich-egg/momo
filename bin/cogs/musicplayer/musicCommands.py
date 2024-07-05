import discord
from discord.ext import commands
import typing
import re
from ..basic.custom_msg import expected_args
from .audio import ytdl_audio
from .options import url_pattern, FFMPEG_OPTIONS


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

    ######################### stop Music ############################################################
    @commands.command()
    @commands.guild_only()
    async def stop(self, ctx: commands.Context):
        try:
            print("is playing", ctx.voice_client.is_playing())
            if ctx.voice_client is None or ctx.voice_client.is_playing() is False:
                return await ctx.send("Song is not playing to stop")
            ctx.voice_client.stop()
        except Exception as e:
            return await ctx.send(f"Error on stop. {e}")

    ######################### pause Music ############################################################
    @commands.command()
    @commands.guild_only()
    async def pause(self, ctx: commands.Context):
        try:
            if ctx.voice_client is None:
                return await ctx.send("Song is not playing to pause")
            ctx.voice_client.pause()
        except Exception as e:
            return await ctx.send(f"Error on stop. {e}")

    ######################### resume Music ############################################################
    @commands.command()
    @commands.guild_only()
    async def resume(self, ctx: commands.Context):
        try:
            print(ctx.voice_client)
            if ctx.voice_client is None or ctx.voice_client.is_paused() is False:
                return await ctx.send("Song is not paused to resume")
            ctx.voice_client.resume()
        except Exception as e:
            return await ctx.send(f"Error on stop. {e}")
