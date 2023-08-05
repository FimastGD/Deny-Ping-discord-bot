import web
import constants as const
import disnake
import os 
from disnake.ext import commands
import asyncio

bot = commands.Bot(command_prefix='dp!', intents=disnake.Intents.all(), help_command=None)

@bot.event
async def on_ready(): 
    activity = disnake.Activity(name="dp!help", type=disnake.ActivityType.playing)
    await bot.change_presence(activity=activity, status=disnake.Status.idle)
    print('Bot is ready!')




server_lang = {}
user1 = {}
user2 = {}
user3 = {}
user4 = {}
user5 = {}


@bot.event
async def on_guild_join(guild):
    server_lang[guild.id] = "en"
    user1[guild.id] = "0" 
    user2[guild.id] = "0" 
    user3[guild.id] = "0"
    user4[guild.id] = "0"
    user5[guild.id] = "0"
@bot.event
async def on_guild_remove(guild):
    del server_lang[guild.id]
    del user1[guild.id]
    del user2[guild.id]
    del user3[guild.id]
    del user4[guild.id]
    del user5[guild.id]

# ===== DELETE MESSAGE AFTER PING ===== #
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    us1 = user1.get(message.guild.id)
    us2 = user2.get(message.guild.id)
    us3 = user3.get(message.guild.id)
    us4 = user4.get(message.guild.id)
    us5 = user5.get(message.guild.id)

    if f"<@{us1}>" in message.content or f"<@{us2}>" in message.content or f"<@{us3}>" in message.content or f"<@{us4}>" in message.content or f"<@{us5}>" in message.content:
        await message.delete()
        author_id = message.author.id
        lang = server_lang.get(message.guild.id)
        response_text = ""
        if lang == "ru":
            response_text = "извините, но вы не можете пинговать данного пользователя"
        elif lang == "en":
            response_text = "sorry, you can't ping this user"
        response = await message.channel.send(f"<@{author_id}> " + response_text)
        await asyncio.sleep(5)
        await response.delete()

    await bot.process_commands(message)

# ===== COMMAND ERROR ===== #
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        lang = server_lang.get(ctx.guild.id)
        
        if lang == "ru":
            embed = disnake.Embed(title=f"{const.ERROR_EMOJI} Ошибка", description="**Неизвестная команда. Напишите **`dp!help`** для помощи**", color=disnake.Color.red())
        elif lang == "en":
            embed = disnake.Embed(title=f"{const.ERROR_EMOJI} Error", description="**Unknown command. Type **`dp!help`** to help**", color=disnake.Color.red())

        await ctx.send(embed=embed)




# ===== LANGUAGE SETUP ===== #

@bot.command()
async def setlang(ctx, value: str = "empty"):
    author = ctx.author
    
    if author.guild_permissions.administrator:
        if value == "ru" or value == "en":
            server_lang[ctx.guild.id] = value
            
        lang = server_lang.get(ctx.guild.id)
        # debug
        print("[LOG] " + lang)
        
        if value == "ru":
            dec_value = "Русский"
            desc_ru_succ = f"**Язык бота изменён на {dec_value}**"
            success_ru = disnake.Embed(title="**Успешно**", description=desc_ru_succ, color=disnake.Color.green())
            await ctx.send(embed=success_ru)
        
        elif value == "en":
            server_lang[ctx.guild.id] = value
            dec_value = "English"
            desc_en_succ = f"**Bot language changed to {dec_value}**"
            success_en = disnake.Embed(title="**Success**", description=desc_en_succ, color=disnake.Color.green())
            await ctx.send(embed=success_en)
        else:
            if lang == "ru":
                emp_desc = "**Введите __dp!setlang <lang>__\nВ <lang> вы можете ввести `ru` или `en` для смены соответствующего языка**"
                emp_emb = disnake.Embed(title="Правильное использование", description=emp_desc, color=disnake.Color.blue())
                await ctx.send(embed=emp_emb)
            elif lang == "en":
                emp_desc = "**Enter __dp!setlang <lang>__\nIn <lang> you can write `en` (English) or `ru` (Russian)**"
                emp_emb = disnake.Embed(title="Right use", description=emp_desc, color=disnake.Color.blue())
                await ctx.send(embed=emp_emb)
    else:
        if value == "en":
            np = "**You don't have any permissions to use this command**"
            np_en = disnake.Embed(title="Error", description=np, color=disnake.Color.red())
            await ctx.send(embed=np_en)
        elif value == "ru":
            np = "**У вас нехватает прав для использования данной команды**"
            np_ru = disnake.Embed(title="Ошибка", description=np, color=disnake.Color.red())
            await ctx.send(embed=np_ru)

# ===== DENY PING MAIN ===== #

@bot.command()
async def denyping(ctx, id: int = 0, userid: int = 0):
    author = ctx.author
    if author.guild_permissions.administrator:
        lang = server_lang.get(ctx.guild.id)
        print(lang)
        if id > 5:
            #err_desc_5s = ""
            #err_tit_5s = ""
            if lang == "ru":
                err_desc_5s = "**Вы не можете запретить пинг больше 5 пользователей на сервере**"
                err_tit_5s = "**Ошибка**"
                err_emb_5s = disnake.Embed(title=err_tit_5s, description=err_desc_5s, color=disnake.Color.red())
                await ctx.send(embed=err_emb_5s)
            elif lang == "en":
                err_desc_5s = "**You can't prevent more than 5 users from ping on a server**"
                err_tit_5s = "**Error**"
                err_emb = disnake.Embed(title=err_tit_5s, description=err_desc_5s, color=disnake.Color.red())
                await ctx.send(embed=err_emb)
        elif userid == 0 or id == 0:
            if lang == "ru":
                all_desc = "**Введите __dp!denyping <id в списке> <user id>.__\n- Примечание: id в списке - номер непингованных пользователей. МАКСИМУМ: 5**"
                all_emb = disnake.Embed(title="Правильное использование", description=all_desc, color=disnake.Color.blue())
                await ctx.send(embed=all_emb)
            elif lang == "en":
                all_desc = "**Enter __dp!denyping <id in list> <user id>__\n- Note: id in list - Number of users who cannot be pinged. MAX: 5**"
                all_emb = disnake.Embed(title="Right use", description=all_desc, color=disnake.Color.blue())
                await ctx.send(embed=all_emb)
        else:
            if id == 1:
                user1[ctx.guild.id] = userid
            elif id == 2:
                user2[ctx.guild.id] = userid
            elif id == 3:
                user3[ctx.guild.id] = userid
            elif id == 4:
                user4[ctx.guild.id] = userid
            elif id == 5:
                user5[ctx.guild.id] = userid
            if lang == "ru":
                succ_desc = f"**Вы запретили пинговать пользователя <@{userid}>**"
                succ_emb = disnake.Embed(title="Успешно", description=succ_desc, color=disnake.Color.green())
                await ctx.send(embed=succ_emb)
            elif lang == "en":
                succ_desc = f"**You have prevented the user from being pinged <@{userid}>**"
                succ_emb = disnake.Embed(title="Success", description=succ_desc, color=disnake.Color.green())
                await ctx.send(embed=succ_emb)
    else:
        if lang == "ru":
            np_desc = "**У вас недостаточно прав для использования данной команды**"
            np_emb = disnake.Embed(title="Ошибка", description=np_desc, color=disnake.Color.red())
            await ctx.send(embed=np_emb)
        elif lang == "en":
            np_desc = "**You don't have any permissions to use this command**"
            np_emb = disnake.Embed(title="Error", description=np_desc, color=disnake.Color.red())
            await ctx.send(embed=np_emb)

# ===== CRON ===== #
@bot.command()
async def cron(ctx):
    author = ctx.author
    if author.guild_permissions.administrator:
        cron1 = const.CRON1
        cron2 = const.CRON2
        cron3 = const.CRON3
        cron4 = const.CRON4
        cron5 = const.CRON5
        noperm = const.NOPERMCRON
    
        embed = disnake.Embed(title="CRON Job", color=disnake.Color.blue(), description=cron1)
        message = await ctx.send(embed=embed)
    
        await asyncio.sleep(1)
        embed.description = cron2
        await message.edit(embed=embed)
    
        await asyncio.sleep(1)
        embed.description = cron3
        await message.edit(embed=embed)
        server_lang[ctx.guild.id] = "en"
    
        await asyncio.sleep(1)
        embed.description = cron4
        await message.edit(embed=embed)
        user1[ctx.guild.id] = "0" 
        user2[ctx.guild.id] = "0" 
        user3[ctx.guild.id] = "0" 
        user4[ctx.guild.id] = "0" 
        user5[ctx.guild.id] = "0"
        ## <debug>
        print(user1)
        print(user2) 
        print(user3)
        print(user4)
        print(user5)
        ## </debug>
    
        await asyncio.sleep(0.5)
        embed.color = disnake.Color.green()
        embed.description = cron5
        await message.edit(embed=embed)
    else:
        cron1 = const.CRON1
        noperm = const.NOPERMCRON
        err_emb = disnake.Embed(title="CRON Job", description=cron1, color=disnake.Color.blue())
        error_msg = await ctx.send(embed=err_emb)
        await asyncio.sleep(2)
        err_emb.description = noperm
        err_emb.color = disnake.Color.red()
        await error_msg.edit(embed=err_emb)


# ===== DENYNPING LIST ===== #
@bot.command()
async def list(ctx):
    

    u1 = user1.get(ctx.guild.id)
    u2 = user2.get(ctx.guild.id) 
    u3 = user3.get(ctx.guild.id)
    u4 = user4.get(ctx.guild.id)
    u5 = user5.get(ctx.guild.id)
    lang = server_lang.get(ctx.guild.id)
    du1 = ""
    du2 = ""
    du3 = ""
    du4 = ""
    du5 = ""
    
    if u1 == "0":
        du1 = "N/A"
    elif u2 == "0":
        du2 = "N/A"
    elif u3 == "0":
        du3 = "N/A"
    elif u4 == "0":
        du4 = "N/A"
    elif u5 == "0":
        du5 = "N/A"

    if u1 != "0":
        du1 = "<@" + {u1} + ">"
    elif u2 != "0":
        du2 = "<@" + {u2} + ">"
    elif u3 != "0":
        du3 = "<@" + {u3}> + ">"
    elif u4 != "0":
        du4 = "<@" + {u4} + ">"
    elif u5 != "0":
        du5 = "<@" + {u5} + ">"

    
    if lang == "en":
        tit = "Deny Ping list"
    elif lang == "ru":
        tit = "Список Deny Ping пользователей"
    embed = disnake.Embed(title=tit, description="**WARNING: THIS FEATURE IN ACTIVE DEVELOPMENT!!!!!**", color=disnake.Color.blue())
    await ctx.send(embed=embed)
    
# ===== HELP ===== #
@bot.command()
async def help(ctx):
    lang = server_lang.get(ctx.guild.id)
    if lang == "ru":
        embed = disnake.Embed(
            title="Deny Ping Info",
            color=disnake.Color.blue(),
            description="**Данный бот позволяет запретить пинг некоторых пользователей**\n\n**__Команды__**\n"
                        "**dp!setlang** - Изменить язык бота\n**dp!list** - Список пользоваелей, которых нельзя пинговать\n"
                        "**dp!denyping** - Запретить пинг пользователей на сервере \n**dp!cron** - Запустить фикс бота на сервере"   
        )
        embed2 = disnake.Embed(title="Предупреждение", description="**Настоятельно рекомендуем прописать `dp!cron` после добавления на сервер**", color=disnake.Color.yellow())
    else:
        embed = disnake.Embed(
            title="Deny Ping Info",
            color=disnake.Color.blue(),
            description="**This bot allows you to prohibit the ping of some users**\n\n**__Commands__**\n"
                        "**dp!setlang** - Change bot language\n**dp!list** - List of users who can't be pinged\n"
                        "**dp!denyping** - Deny ping for users on server\n**dp!cron** - Fix bot bugs in server"
        )
        embed2 = disnake.Embed(title="Alert", description="We strongly recommend that you register 'dp!cron' after adding the bot to the server", color=disnake.Color.yellow())

    await ctx.send(embed=embed)
    await ctx.send(embed=embed2)


# ===== CHANGE LANGUAGE [BETA AND UNTESTED!!!!! IT MAY NOT WORKING!!!!!] ===== #
@bot.command()
@commands.has_permissions(administrator=True)
async def setbetalang(ctx):
    
    
    author = ctx.author
    serverlang = server_lang.get(ctx.guild.id)

    if author.id == ctx.message.author.id:
        if serverlang == 'en':
            embed = disnake.Embed(color=disnake.Color.blue(), title="**Select language**", description=f"**__Default language:__ English\n__Current language:__ English**\nClick on button to change language.")
        elif serverlang == 'ru':
            embed = disnake.Embed(color=disnake.Color.blue(), title="**Выберите язык**", description=f"**__Язык по умолчанию:__ English\n__Текущий язык:__ Русский**\nНажмите на кнопку для смены языка.")

        en_button = disnake.Button(style=disnake.ButtonStyle.blurple, label="English", emoji="🇺🇸", custom_id="en")
        ru_button = disnake.Button(style=disnake.ButtonStyle.blurple, label="Русский", emoji="🇷🇺", custom_id="ru")

        action_row = disnake.ActionRow(en_button, ru_button)

        message = await ctx.send(embed=embed, components=action_row)

        def check(inter):
            return inter.user.id == author.id

        try:
            inter = await bot.wait_for("button_click", timeout=None, check=check)
            if inter.component.custom_id == "en":
                serverlang = 'en'
                server_lang[ctx.guild.id] = serverlang
                
                success_embed = disnake.Embed(color=disnake.Color.green(), title="Success", description="**Language changed to __English__**")
                await inter.response.send_message(embed=success_embed, ephemeral=True)
            elif inter.component.custom_id == "ru":
                serverlang = 'ru'
                server_lang[ctx.guild.id] = serverlang
                success_embed = disnake.Embed(color=disnake.Color.green(), title="Успешно", description="**Язык успешно изменён на: __Русский__**")
                await inter.response.send_message(embed=success_embed, ephemeral=True)
        except disnake.errors.InteractionTimedOut:
            await message.delete()
            await ctx.send("Ошибка: вы не можете взаимодействовать с данными кнопками", delete_after=10.0)

    else:
        if serverlang != 'ru':
            error_embed = disnake.Embed(color=disnake.Color.red(), title="ERROR", description="**You don't have permissions to use this command!**")
            await ctx.send(embed=error_embed)
        elif serverlang == 'ru':
            error_embed = disnake.Embed(color=disnake.Color.red(), title="ОШИБКА", description="**У вас нет разрешений на использование данной команды!**")
            await ctx.send(embed=error_embed)

 

web.start()
bot.run(const.TOKEN)
