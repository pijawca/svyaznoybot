# -*- coding: utf-8 -*-
from disnake.ext import commands
from config import TOKEN
import disnake
import logging


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

bot = commands.Bot(command_prefix='!', help_command=None, intents=disnake.Intents.all())
