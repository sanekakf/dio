import discord
from discord.ext import commands
from random import randint
import sqlite3 as qs

import sqlite3 as qs
conn = qs.connect("dio.db")
cur = conn.cursor()

class muda(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

#https://i.imgur.com/oNcHdPX.gif
    @commands.command(name = "attack",
                    aliases=['atack','attac','atac','atak','attak'],
                    usage="@user",
                    description = "Использует станд ДЫО что бы нанести урон, а также выбить с человека монет (наносит неопределенный урон, а также можно получить монеты зависящие от стэнда)")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 480, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context, member:discord.Member=None):
        if member is None:
            await ctx.send(f'Вы не можете атковать себя, {ctx.author.mention}')
        else:
            st=cur.execute("SELECT soul FROM inventory WHERE userId LIKE ?", (ctx.author.id,))
            for s in st:
                stand=s[0]
            if stand=='Za_Warudo':
                damage=randint(7,20)
                money=randint(10,15)
                url='https://i.imgur.com/oNcHdPX.gif'
            elif stand=='Star_Platina':
                damage=randint(10,18)
                money=randint(5,14)
                url='https://media.tenor.com/images/95fadce08619136ec90dc820aaf405a1/tenor.gif'
            elif stand=='King_Krimson':
                damage=randint(2,19)
                money=randint(1,20)
                url='https://media.tenor.com/images/d1ea616b7938df8301f344580b122e77/tenor.gif'
            else:
                damage=randint(1,5)
                money=randint(2,8)
            h=cur.execute('SELECT health FROM player WHERE userId LIKE ?', (ctx.author.id,))
            for mlg in h:
                if mlg[0] <= 0:
                    await ctx.send('Вы не можете использовать атакующие способности будучи мертвым')
            else:
                health=cur.execute('SELECT health FROM player WHERE userId LIKE ?', (member.id,))
                for hp in health:
                    n_health=hp[0]-damage
                    print(n_health)
                    cur.execute(f'UPDATE player SET health = {n_health} WHERE userId LIKE ?',(member.id,))
                    conn.commit()
                    if stand != 'Стандартный':
                        embed=discord.Embed(
                            title=f'{ctx.author.name} произвел атаку на {member.name} используя станд {stand}',
                            description=f'Хп {member.name} теперь {n_health}'
                        )
                        embed.set_image(url=url)
                    else:
                        embed=discord.Embed(
                            title=f'{ctx.author.name} произвел атаку на {member.name} используя камень',
                            description=f'Хп {member.n_money} теперь {n_health}'
                        )
                    await ctx.send(embed=embed)
                    x=cur.execute('SELECT money FROM player WHERE userId LIKE ?', (ctx.author.id,))
                    for row in x:
                        cmoney=row[0]
                        n_money= cmoney + money
                        cur.execute(f'UPDATE player SET money = {n_money} WHERE userId LIKE ?', (ctx.author.id,))
                        conn.commit()
                        await ctx.send(f'Полученно монет: {money}')
                        await ctx.send(f'Нанесено урона: {damage}')
                        cur.execute('SELECT money FROM player WHERE userId LIKE ?' , (ctx.author.id,))
                        mon=cur.fetchall()
                        print(f'Money {ctx.author.name}: {mon[0][0]}')
import discord
from discord.ext import commands


class heal(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "heal",
                    usage="@user",
                    description = "Используя станд King_Krimson отматывайте время и исцеляте пользователя на 32 хп")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 120, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context, member:discord.Member=None):
        if member is None:
            await ctx.send('Вы забыли ввести пользователя который будет исцелен. *d.heal @dio\'s*')
        else:
            h=cur.execute('SELECT health FROM player WHERE userId LIKE ?' , (member.id,))
            for health in h:
                hp=health[0]
            sg=cur.execute('SELECT soul FROM inventory WHERE userId LIKE ?', (ctx.author.id,))
            for stands in sg:
                N_healt=hp+32
                print(stands[0])
                if stands[0] == 'King_Krimson':
                    cur.execute('UPDATE player SET health = ? WHERE userId LIKE ?',(N_healt,member.id))
                    conn.commit()
                    embed=discord.Embed(title="Исцеление", description=f"От {ctx.author.name}", color=0xff5200)
                    embed.add_field(name=f"{ctx.author.name} используя King_Krimson исцелил {member.name}", value=f"{member.name} хп теперь: {N_healt}", inline=False)
                    await ctx.send(embed=embed)
                else:
                    await ctx.send('Вы не можете исцелять без King_Krimson')

# def setup(bot:commands.Bot):
def setup(bot:commands.Bot):
    bot.add_cog(heal(bot))
    bot.add_cog(muda(bot))