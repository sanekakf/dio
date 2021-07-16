import discord
from discord.ext import commands
from random import randint

class HelpCog(commands.Cog, name="help command"):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
  

	@commands.command(name = 'help',
					usage="(Имя Комманды)",
					description = "Показывает помощь.",
					aliases = ['h', '?'])
	@commands.cooldown(1, 2, commands.BucketType.member)
	async def help (self, ctx, commandName:str=None):

		commandName2 = None
		stop = False

		if commandName is not None:
			for i in self.bot.commands:
				if i.name == commandName.lower():
					commandName2 = i
					break 
				else:
					for j in i.aliases:
						if j == commandName.lower():
							commandName2 = i
							stop = True
							break
						if stop is True:
							break 

			if commandName2 is None:
				await ctx.channel.send("Комманда не найдена")   
			else:
				embed = discord.Embed(title=f"{commandName2.name.upper()}", description="", color=randint(0, 0xffffff))
				embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
				embed.add_field(name=f"Имя", value=f"{commandName2.name}", inline=False)
				aliases = commandName2.aliases
				aliasList = ""
				if len(aliases) > 0:
					for alias in aliases:
						aliasList += alias + ", "
					aliasList = aliasList[:-2]
					embed.add_field(name=f"Альтернативы", value=aliasList)
				else:
					embed.add_field(name=f"Альтернативы", value="None", inline=False)

				if commandName2.usage is None:
					embed.add_field(name=f"С чем она используется", value=f"None", inline=False)
				else:
					embed.add_field(name=f"Использование", value=f"{self.bot.command_prefix}{commandName2.name} {commandName2.usage}", inline=False)
				embed.add_field(name=f"Описание", value=f"{commandName2.description}", inline=False)
				await ctx.channel.send(embed=embed)             
		else:
			embed = discord.Embed(title=f"Страничка помощи", description=f"{self.bot.command_prefix}help (Имя комманды), показывает список помощи или помощь с определенной коммандой.", color=randint(0, 0xffffff))
			embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
			for i in self.bot.commands:
				embed.add_field(name=i.name, value=i.description, inline=False)
			await ctx.channel.send(embed=embed)

def setup(bot:commands.Bot):
	bot.remove_command("help")
	bot.add_cog(HelpCog(bot))
