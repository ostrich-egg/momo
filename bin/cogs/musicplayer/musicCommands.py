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

response_array = []


class musicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ######################### __Player (not commands) ############################################################

    async def _player(self, ctx: commands.Context):
        try:
            if len(response_array) == 0:
                return

            response = response_array.pop(0)

            ## create event loop to play queued song
            def _after():
                self.bot.loop.create_task(self._player(ctx))

            ## play
            ctx.voice_client.play(
                discord.FFmpegPCMAudio(response["url"], **FFMPEG_OPTIONS),
                after=lambda e: _after(),
            )

            text = re.sub(re.compile(r"(?<=\b\w) (?=\w\b)"), "", response["title"])

            await ctx.send(
                f"Now playing  :loudspeaker:   : *{"".join((text.split("  ")))}*"
            )

        except Exception as e:
            await ctx.send(f"Error on _q {e}")

    ######################### __Queue Music (not commands) ############################################################
    async def _q(self, ctx: commands.Context, *, song=None):
        try:
            # checkif it is url
            type = "url" if url_pattern.search(song) else "text"
            Queued = False

            # checking if queue
            if ctx.voice_client.is_playing() or len(response_array) > 1:
                Queued = True
                await ctx.send(
                    f":small_blue_diamond: Added to queue no: {len(response_array) + 1} "
                )

            # appending to array
            response_array.append(ytdl_audio(song, type))

            if Queued:
                return
            # calling to play
            await self._player(ctx)

        except Exception as e:
            await ctx.send(f"Error on _q {e}")

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
                await ctx.send(f"I am at :  {channel}")
                return await ctx.voice_client.move_to(channel=channel)

            await channel.connect()
            return await ctx.send(f"Joined channel **{channel}**")

        except Exception as e:
            return await ctx.send(f"Cannot join. {e}")

    ######################### Play Music ############################################################
    @commands.command()
    @commands.guild_only()
    @commands.Cog.listener()
    async def play(
        self,
        ctx: commands.Context,
        *,
        song=None,
    ):
        try:
            # checkers
            if ctx.voice_client is None:
                return await ctx.send("Allow me to join voice channel first")

            if song is None:
                return await ctx.send(embed=expected_args("!play \n*[title or url]*"))

            # call for Queue
            await self._q(ctx, song=song)

        except Exception as e:
            return await ctx.send(f"Error on playing {e}")

    ######################### stop Music ############################################################
    @commands.command()
    @commands.guild_only()
    async def stop(self, ctx: commands.Context):
        try:
            if ctx.voice_client is None or ctx.voice_client.is_playing() is False:
                return await ctx.send("Song is not playing to stop")

            ctx.voice_client.stop()
            await ctx.send(f"Music stopped by *{ctx.author}*")

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
            await ctx.send(f"Music paused by *{ctx.author}*")

        except Exception as e:
            return await ctx.send(f"Error on stop. {e}")

    ######################### resume Music ############################################################
    @commands.command()
    @commands.guild_only()
    async def resume(self, ctx: commands.Context):
        try:
            if ctx.voice_client is None or ctx.voice_client.is_paused() is False:
                return await ctx.send("Song is not paused to resume")

            ctx.voice_client.resume()
            await ctx.send(f"Music resumed by *{ctx.author}*")

        except Exception as e:
            return await ctx.send(f"Error on stop. {e}")
