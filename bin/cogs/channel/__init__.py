from discord.ext import commands
import discord
import typing

from ..basic.custom_msg import expected_args


class Channel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    ######################### Create category ############################################################
    @commands.command()
    @commands.guild_only()
    async def newcategory(self, ctx: commands.Context, name: str = None):
        try:
            if name is None:
                return await ctx.send(
                    embed=expected_args(
                        "!create_cat\n *name of category*", discord.Color.red()
                    )
                )
            await ctx.guild.create_category(name=name)
            return await ctx.send(f"New category created : **{name}**")

        except discord.DiscordException as e:
            await ctx.send(f"An Error occured while creating category {e}")

    ######################### Create new Channel ############################################################
    @commands.command()
    @commands.guild_only()
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

        except discord.DiscordException as e:
            await ctx.send(f"Cannot create channel {e}")

    ######################### Delete Channel ############################################################
    @commands.command()
    @commands.guild_only()
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
                        "!delete\n *channel*",
                        discord.Color.red(),
                    )
                )

            list_channel = []
            for channel in channels:
                list_channel.append(channel.name)
                await channel.delete()
            return await ctx.send(f"Deleted Channel :  **{" ".join(list_channel)}**")

        except discord.DiscordException as e:
            await ctx.send(f"Error on Deleting your request {e}")

    ######################### Delete Category ############################################################
    @commands.command()
    @commands.guild_only()
    async def delcategory(
        self, ctx: commands.Context, category: discord.CategoryChannel = None
    ):
        try:
            if category is None:
                return await ctx.send(
                    embed=expected_args(
                        "!delete\n *category*",
                        discord.Color.red(),
                    )
                )
            await category.delete()
            return await ctx.send(f"Deleted Category **{category}**")
        except discord.DiscordException as e:
            await ctx.send(f"Cannot delete category {e}")


######################### Setup ##################################################################
async def setup(bot: commands.Bot):
    await bot.add_cog(Channel(bot))
