import discord


def discord_print(title="Commands", description="", colour=discord.Color.blurple()):
    embed = discord.Embed(
        title=title,
        description=description,
        color=colour,
    )
    return embed


def expected_args(Args, color=discord.Color.red()):
    embed = discord_print("Expected Args:", Args, color)
    return embed
