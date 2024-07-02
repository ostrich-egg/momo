import discord
from discord.ext import commands
import random
import aiohttp

# import typing
import dotenv
import os

dotenv.load_dotenv()
GIF_TOKEN = os.getenv("GIF_TOKEN")


welcome_messages = [
    "We hope you brought coke and pizza. 🍕",
    "We were all waiting for you... not really, but it's nice to have you here!",
    "You finally made it! We're still waiting for your mixtape to drop. 🔥",
    "You just leveled up by joining us. 🆙",
    "Alert! has landed! Brace yourselves for epicness! 🚀",
    "We hope you survive the experience. 😜",
    "May your memes be dank and your games be epic! 🎮",
    "Joining this server gives you +10 cool points! 🆒",
    "We've been expecting you... Your quest begins now! 🗡️",
    "Resistance is futile. You have been assimilated into the server. 🤖",
    "Hope you brought snacks because we're all out. 🍿",
    "You're officially cooler now because you're here. 😎",
]
greeting_words = [
    "hello",
    "hi",
    "hey",
    "welcome",
    "greetings",
    "salutations",
    "howdy",
    "hi there",
    "good to see you",
    "pleased to meet you",
    "nice to meet you",
    "great to see you",
    "how’s it going",
    "what’s up",
    "glad you're here",
    "good day",
    "ahoy",
    "yo",
    "hiya",
    "bonjour",
    "exciting",
    "thrilled",
    "ecstatic",
    "pumped",
    "enthusiastic",
    "overjoyed",
    "delighted",
    "stoked",
    "elated",
    "buzzing",
]


async def api_call():
    if not GIF_TOKEN:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://api.giphy.com/v1/stickers/search",
            params={
                "q": random.choice(greeting_words),
                "api_key": GIF_TOKEN,
                "limit": 1,
            },
        ) as response:
            if response.status == 200:
                data = await response.json()
                # print("data", data)
                gif_url = (
                    data["data"][0]["images"]["original"]["url"]
                    if data["data"]
                    else "welcome . gif"
                )
                return gif_url
            else:
                return None


async def template(member):
    return discord.Embed(
        title="",
        description=f"Welcome! {member}. {random.choice(welcome_messages)}. ",
    )


##########################################################################################################
###################################### ---Command Class--- ###############################################
##########################################################################################################


class ClientListener(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_join(self, member: discord.User):
        channel = member.guild.system_channel
        if channel:
            embed = await template(member.mention)
            url = await api_call()

            if url:
                embed.set_thumbnail(url=url)
            return await channel.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(ClientListener(bot))
