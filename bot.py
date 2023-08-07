# -*- coding: utf-8 -*-
from misc import bot
from handlers import general
import config
import db
    

if __name__ == '__main__':
    bot.run(token = config.TOKEN)
    db.create_table()
    