import discord
from discord_components import DiscordComponents
from discord.ext import commands
import json
import os
import sqlite3 as qs

conn = qs.connect("dio.db")
cur = conn.cursor()

# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]

cur.execute(
    """CREATE TABLE IF NOT EXISTS player(
    userId INT PRIMARY KEY,
    name TEXT,
    health INT,
    money INT);"""
)
cur.execute("""
	CREATE TABLE IF NOT EXISTS shop(
    tovarname TEXT PRIMARY KEY,
    mon INT);"""
)
cur.execute("""
	CREATE TABLE IF NOT EXISTS inventory(
	userId INT PRIMARY KEY,
	soul TEXT)
""")
conn.commit()
x=150
cur.execute(f"UPDATE player SET money = {x} WHERE userId LIKE ?", (447030106179764226,))
conn.commit()
# cur.execute('DELETE FROM shop WHERE tovarname LIKE ?', ("Стрела",))
# conn.commit()
# name='Стрела'
# money = 125
# tovar=(name,money)
# cur.execute("INSERT INTO shop VALUES(?,?)", tovar)
# conn.commit()

class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents
intents = discord.Intents.default()
# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

# Load cogs
if __name__ == '__main__':
	for filename in os.listdir("Cogs"):
		if filename.endswith(".py"):
			bot.load_extension(f"Cogs.{filename[:-3]}")

@bot.event
async def on_ready():
	DiscordComponents(bot)
	cur.execute('SELECT * FROM PLAYER')
	players=cur.fetchall()
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	print(players)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

bot.run(token)
