import discord
from discord.ext import commands
import time


class PingCog(commands.Cog, name="ping command"):
	def __init__(self, bot:commands.bot):
		self.bot = bot
        
	@commands.command(name = "ping",
					usage="",
					description = "Отображает пинг.")
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def ping(self, ctx):
		before = time.monotonic()
		message = await ctx.send("🏓 Понг !")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f"🏓 Понг !  `{int(ping)} ms`")

def setup(bot:commands.Bot):
	bot.add_cog(PingCog(bot))