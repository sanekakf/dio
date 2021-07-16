import discord
from discord.ext import commands
import sqlite3 as qs

conn = qs.connect("dio.db")
cur = conn.cursor()


class New_player(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="new",
        usage="@user",
        description="Позволяет вам использовать полный функционал бота",
    )
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx: commands.Context, member: discord.Member = None):
        if member is None:
            await ctx.send("После комманды нужно ввести себя : d.new <@!865212733807788062>")
        else:
            from random import randint

            userid = member.id
            name = member.name
            health = 100
            money = 0
            stand='Стандартный'
            user = (int(userid), name, health, money)
            cur.execute("INSERT INTO player VALUES(?,?,?,?)", user)
            conn.commit()
            inventory=(userid,stand)
            cur.execute("INSERT INTO inventory VALUES(?,?)", inventory)
            conn.commit()
            embed = discord.Embed(
                title=f"Пользователь {member.name},был успешно добавлен",
                description="   ",
                color=randint(0, 0xFF0000),
            )
            # embed.set_author(name="name", url="url", icon_url="icon")
            embed.set_thumbnail(url=f"{member.avatar_url}")
            embed.add_field(
                name="Новый человек в нашей ЖиЖе",
                value=f"{member.name}, \
                    теперь тебе доступен полный функционал",
                inline=False,
            )
            embed.set_footer(text="DIO доволен")
            await ctx.send(embed=embed)


import discord
from discord.ext import commands


class delete(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(
        name="delete",
        usage="@user",
        aliases=['del','dl'],
        description="Удаляет вас с этой деревушки, функционал обрезается",
    )
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx: commands.Context,member: discord.Member = None, password:int=1):
        if password != 1234:
            await ctx.send('Забудь про это комманду')
        else:
            if member is None:
                await ctx.send("Вы забыли ввести себя вместе с коммандой : d.delete @dio's")
            else:
                cur.execute("DELETE FROM player WHERE userId LIKE ?", (member.id,))
                conn.commit()
                cur.execute("DELETE FROM inventory WHERE userId LIKE ?", (member.id,))
                conn.commit()
                print(f"{member.name} was deleted")
                cur.execute("SELECT * FROM player")
                players = cur.fetchall()
                print(players)
                await ctx.send(
                    f"Пользователь {member.name} был выгнан с деревушки, теперь ему ограничен полный функционал к ботам :'("
                )
import discord
from discord.ext import commands


class find_plyer(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "fetch",
                    usage="@user",
                    description = "Находит пользователя и выводит его статистику")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context, member: discord.Member= None):
        if member is None:
            await ctx.send('Вы забыли ввести человека вместе с коммандой : d.fetch @dio\'s')
        else:
            x=cur.execute('SELECT * FROM player WHERE name LIKE ?', (member.name,))
            for row in x:
                if row[2]<=0:
                    embed= discord.Embed(
                        title=f'Информация о игроке {member.name}',
                        description=f'Его х: {row[2]}',
                        color=0x000000
                    )
                    embed.set_author(
                        name=f'{row[1]}', icon_url=f'{member.avatar_url}'
                    )
                    embed.set_thumbnail(url=f'{member.avatar_url}')
                    embed.add_field(
                        name=f'{member.name} больше не дышит',
                        value='Помер...',
                        inline=False
                    )
                    embed.set_image(
                        url='https://media.discordapp.net/attachments/695285114099466251/862153466449494036/unknown.png'
                    )
                    await ctx.send(embed=embed)
                else:
                    gh=cur.execute('SELECT soul FROM inventory WHERE userId LIKE ?', (member.id,))
                    for sbs in gh:
                        standh=sbs[0]
                        from random import randint
                        embed=discord.Embed(
                            title=f'Информация о игроке {member.name}',
                            description=f'Его хп: {row[2]}, деньги - {row[3]}',
                            color=randint(0, 0xFF0000)
                        )

                        embed.add_field(
                            name=f'Инвентарь {member.name}',
                            value=f'Стэнд: {standh}',
                            inline=False
                        )
                        embed.set_author(
                            name=f'{row[1]}', icon_url=f'{member.avatar_url}'
                        )
                        embed.set_thumbnail(
                            url=f'{member.avatar_url}'
                        )
                        # embed.set_footer(text='Это бета версия, ночью будут доработки')
                        embed.set_image(
                            url="https://cdn.discordapp.com/attachments/861649193722839050/862123107086630953/Screenshot_20210707-030757_Chrome_1.jpg"
                        )
                        if standh != 'Стандартный':
                            if standh=='Za_Warudo':
                                url='http://pm1.narvii.com/7372/899ee4ca98d3bcc738fce5d317ad6fa16aa3b824r1-687-874v2_uhq.jpg'
                            elif standh =='Star_Platina':
                                url='https://media.discordapp.net/attachments/861649193722839050/865664573112844328/unknown.png?width=386&height=499'
                            elif standh == 'King_Krimson':
                                url='https://cdn.discordapp.com/attachments/861649193722839050/865665151779471420/unknown.png'
                            embed.add_field(
                                name=f'Стэнд {member.name}: {standh}',
                                value='Dio\'s завидует'
                            )
                            embed.set_image(
                                url=url
                            )
                        await ctx.send(embed=embed)
                    
def setup(bot: commands.Bot):
    bot.add_cog(find_plyer(bot))
    bot.add_cog(delete(bot))
    bot.add_cog(New_player(bot))
