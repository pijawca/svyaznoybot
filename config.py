from disnake.ext import commands
import disnake


TOKEN = '#'

DB_NAME = 'svyaznoybot'

cookies = {
    '_ym_isad': '1',
    '_ym_d': '1690901420',
    '_ym_uid': '1690901420743706632',
}

headers = {
    # 'Cookie': '_ym_isad=1; _ym_d=1690901420; _ym_uid=1690901420743706632',git
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'Host': 'wotomatic.net',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.2 Safari/605.1.15',
    'Accept-Language': 'ru',
    # 'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

help_embed = disnake.Embed(
    title="Помощь",
    description='Привет! Я связной 👀\n'
    'На данный момент бот сырой и имеет баги.\n'
    'А пока ты можешь воспользоваться такими командами как:\n\n'
    '**!reg ваш ник в игре** регистрация в базу данных для игры World of Tanks(пример: /reg pijawca)\n'
    '**!ws** Просмотр своей **статистики** в World of Tanks\n\n'
    '[Посмотреть код на Github](https://github.com/pijawca/svyaznoybot)',
    colour=0xC43FF0,
)
