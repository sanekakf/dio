import discord
from discord.ext import commands
from random import randint

class on_JOEN(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_guild_join(self, guild:discord.Guild):
        x = guild.text_channels
        chann = x[0]
        player=await guild.fetch_member(guild.owner_id)
        embed=discord.Embed(title=f"Спасибо за приглашение", description=f"{player.mention}, ДЫО будет служит верностью и правдой, разбивая ебальники всем остальным", color=randint(0,0xff0000))
        # embed.add_field(name="field", value="value", inline=False)
        await chann.send(embed=embed)


def setup(bot:commands.Bot):
    bot.add_cog(on_JOEN(bot))