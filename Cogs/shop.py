import discord
from discord_components import DiscordComponents,Button, Select, SelectOption, component, interaction
from discord.ext import commands
import sqlite3 as qs
from random import choices

conn = qs.connect("dio.db")
cur = conn.cursor()

stands=['Za_Warudo','Star_Platina', 'King_Krimson',]
ch=choices(stands)

class shop(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot


    @commands.command(name = "shop",
                    usage="",
                    description = "Показывает магазин")
    @commands.guild_only()
    @commands.has_permissions()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def commandName(self, ctx:commands.Context):
        row=cur.execute('SELECT money FROM player WHERE userId LIKE ?', (ctx.author.id,))
        for money in row:
            print(money[0])
        row=cur.execute('SELECT * FROM shop')
        for tovars in row:
            arrow=tovars[0]
            price=tovars[1]
        embed=discord.Embed(
            title='Спасибо что зашли к нам',
            description=f'Рады тебя видеть {ctx.author.name}, ваш счет = {money[0]}'
        )
        embed.set_thumbnail(url=f'{ctx.author.avatar_url}')
        embed.add_field(
            name='Товары',
            value='Список товаров которые можно купить, выбрав опцию ниже этого сообщения',
            inline=False
        )
        embed.set_image(
            url='https://cdna.artstation.com/p/assets/images/images/018/905/216/large/hanson-lee-picture-2.jpg?1561181355'
        )
        embed.add_field(
            name=f'{arrow}',
            value=f'Данная стрела активирует в вашей душе стэнд\n\nЦена: {price}'
        )
        global disabled, placeholder
        if money[0] >= price:
            disabled=False
            placeholder='Выбирайте со вкусом'
        else:
            placeholder='У вас не хвтает денег на покупку(любую)'
            disabled=True
        await ctx.send(
            embed=embed,
            components=[
                Select(
                    placeholder=placeholder,
                    disabled=disabled,
                    options=[
                        SelectOption(label='Стрела', value='arrow')
                    ]
                ),
                Button(
                    style=component.ButtonStyle.grey,
                    label='Следущая страница',
                    disabled=True
                ),
            ],
            delete_after=12
        )

        while True:
            # s=cur.execute('SELECT stand from inventory WHERE userId LIKE ?', (ctx.author.id,))
            # for sg in s:
                # stand=sg[0]
            inter= await self.bot.wait_for('select_option')
            x=cur.execute('SELECT money FROM player WHERE userId LIKE ?', (ctx.author.id,))
            await inter.respond(content=f'Спасибо за покупку {ctx.author.name}, с вашего счета быо списанно 125$\n\nВаш стэнд: {ch}')
            for mon in x:
                n_money=mon[0]-price
                cur.execute(f'UPDATE player SET money = {n_money} WHERE userId LIKE ?', (ctx.author.id,))
                # conn.commit()
                # print(1)
                # print(2)
                cur.execute(f'UPDATE inventory SET soul = ? WHERE userId LIKE ?' , (ch[0],ctx.author.id,))
                conn.commit()
                cur.execute('SELECT money FROM player WHERE userId LIKE ?', (ctx.author.id,))
                mn=cur.fetchone()
                cur.execute('SELECT * FROM inventory')
                alls=cur.fetchall()
                print(alls)
                print(f'money {ctx.author.name}: {mn[0]}')


def setup(bot:commands.Bot):
    bot.add_cog(shop(bot))