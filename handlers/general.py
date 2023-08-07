# -*- coding: utf-8 -*-
from disnake.ext import commands
from bs4 import BeautifulSoup
from lxml import etree
from misc import bot
from PIL import Image, ImageFont, ImageDraw
from handlers.embed import help_embed
import requests
import psycopg
import disnake
import config
import db
import sys


@bot.event
async def on_ready():
    try:
        await bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(type=disnake.ActivityType.watching))
        print(f'[LOG IN] SUCCESS {bot.user}')
    except:
        print(f'[LOG IN] FAILED {bot.user}')
    
@bot.command()
async def shelp(ctx):
    await ctx.send(embed=help_embed)

@bot.command()
async def reg(ctx, message):
    await ctx.send(f'Секундочку.. Проверяю профиль {message}')
    
    discord = ctx.author
    discord = discord.name
    response = requests.get(f'http://wotomatic.net/?search={message}', cookies=config.cookies, headers=config.headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    dom = etree.HTML(str(soup))
    
    try:
        search = dom.xpath('//*[@id="wrapper"]/p')[0].text
        if search.startswith('ОШИБКА'):
            await ctx.send('Профиль не найден. Убедитесь в правильности ввода') 
        else:
            pass
        
    except IndexError:
        await ctx.send('Ваш профиль был занесен в базу бота. Чтобы посмотреть свою статистику введите !ws')
        
        response = requests.get(f'http://wotomatic.net/?search={message}', cookies=config.cookies, headers=config.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        dom = etree.HTML(str(soup))
        
        conn = psycopg.connect(host='localhost')
        conn.autocommit = True
        
        nickname = dom.xpath('//*[@id="AccountName"]/tr/td/a')[0].text
        nickname = nickname.replace(' ', '')
        
        clan = dom.xpath('//*[@id="ClanTagName"]/tr/td[1]/div/a')[0].text
        clan = (f'[{clan}]')
        
        allbattles = dom.xpath('///*[@id="stAllBattles"]/tr/td[2]')[0].text
        allbattles = allbattles.replace(' ', '')

        allwins = dom.xpath('//*[@id="stAllBattles"]/tr/td[3]/span')[0].text
        allwins = allwins[0:6]

        wn8 = dom.xpath('//*[@id="rateWN8"]/tr/td[3]/span')[0].text

        wgr = dom.xpath('//*[@id="rateWG"]/tr/td[3]/span')[0].text

        eff = dom.xpath('//*[@id="rateEFF"]/tr/td[3]/span')[0].text

        lvl = dom.xpath('//*[@id="LevelAvg"]/tr/td[2]/span')[0].text

        dmg = dom.xpath('//*[@id="DamageAvg"]/tr/td[3]/span')[0].text

        try:
            conn = psycopg.connect(host='localhost')
            with conn.cursor() as cur:
                cur.execute("""INSERT INTO svyaznoybot (
                    nickname, 
                    discord, 
                    clan, 
                    allbattles,
                    allwins,
                    wn8,
                    wgr,
                    eff,
                    lvl,
                    dmg) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING""",
                    (nickname, discord, clan, allbattles, allwins, wn8, wgr, eff, lvl, dmg))
                
                conn.commit()
                conn.close()
                cur.close()
        except psycopg.errors.DuplicateDatabase:
                pass

@bot.command()
async def ws(ctx, user: disnake.Member = None):
    conn = psycopg.connect(host='localhost')
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            user = ctx.author
            user = user.name
            searchNickname = cur.execute("""SELECT nickname FROM svyaznoybot WHERE discord=%s""", [user])
            user = searchNickname.fetchall()
            
            response = requests.get(f'http://wotomatic.net/?search={user[0][0]}', cookies=config.cookies, headers=config.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            dom = etree.HTML(str(soup))
            
            nickname = dom.xpath('//*[@id="AccountName"]/tr/td/a')[0].text
            nickname = nickname.replace(' ', '')
            
            discord = ctx.author
            discord = discord.name
            
            clan = dom.xpath('//*[@id="ClanTagName"]/tr/td[1]/div/a')[0].text
            clan = (f'[{clan}]')
            
            allbattles = dom.xpath('///*[@id="stAllBattles"]/tr/td[2]')[0].text
            allbattles = allbattles.replace(' ', '')

            allwins = dom.xpath('//*[@id="stAllBattles"]/tr/td[3]/span')[0].text
            allwins = allwins[0:6]

            wn8 = dom.xpath('//*[@id="rateWN8"]/tr/td[3]/span')[0].text

            wgr = dom.xpath('//*[@id="rateWG"]/tr/td[3]/span')[0].text

            eff = dom.xpath('//*[@id="rateEFF"]/tr/td[3]/span')[0].text

            lvl = dom.xpath('//*[@id="LevelAvg"]/tr/td[2]/span')[0].text

            dmg = dom.xpath('//*[@id="DamageAvg"]/tr/td[3]/span')[0].text
            
            cur.execute ("""UPDATE svyaznoybot SET 
                        clan = %s, 
                        allbattles = %s,
                        allwins = %s,
                        wn8 = %s,
                        wgr = %s,
                        eff = %s,
                        lvl = %s,
                        dmg = %s;
                        """, (clan, allbattles, allwins, wn8, wgr, eff, lvl, dmg))
            print(user)
            print (f'[{config.DB_NAME}] Был перезаписан профиль {user[0][0]}')
            
            user = ctx.author
            user = user.name
            selectNickname = cur.execute("""SELECT * FROM svyaznoybot WHERE discord=%s""", [user])
            user = selectNickname.fetchall()
            
            try:
                img = Image.open("handlers/raw.png")
            except:
                print('[PILLOW] Не могу открыть изображение')
                sys.exit(1)
            
            idraw = ImageDraw.Draw(img)
            idraw.text((226, 43), text=str(user[0][3]+user[0][2]), font=ImageFont.truetype("handlers/Roboto.ttf", size=16))
            idraw.text((360, 98), text=str(user[0][4]), font=ImageFont.truetype("handlers/Roboto.ttf", size=11))
            idraw.text((360, 136), text=str(user[0][5]), font=ImageFont.truetype("handlers/Roboto.ttf", size=11))
            idraw.text((360, 174), text=str(user[0][6]), font=ImageFont.truetype("handlers/Roboto.ttf", size=11))
            idraw.text((360, 212), text=str(user[0][7]), font=ImageFont.truetype("handlers/Roboto.ttf", size=11))
            idraw.text((360, 250), text=str(user[0][8]), font=ImageFont.truetype("handlers/Roboto.ttf", size=11))
            idraw.text((360, 288), text=str(user[0][9]), font=ImageFont.truetype("handlers/Roboto.ttf", size=11))
            idraw.text((360, 326), text=str(user[0][10]), font=ImageFont.truetype("handlers/Roboto.ttf", size=11))
            img.save('handlers/result.png')
            
            with open('handlers/result.png', 'rb') as file:
                png_file = disnake.File(file, filename='handlers/result.png')
                await ctx.send(file=png_file)
                await ctx.send(embed = disnake.Embed(
                    title=f'Полезные ссылки:',
                    description=f'Внимание! Данная картинка обрабатывается ботом, возможны баги.\nПодробная статистика: https://kttc.ru/wot/ru/user/{user[0][2]}\nУзнать сколько нужно урона до 3-х отметок: https://poliroid.me/gunmarks\nСвежие новости: https://wotexpress.info/news/mir-tankov\nПортал игры LESTA: https://tanki.su'))
                
    except:
        pass
    