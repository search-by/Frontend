from django.apps import AppConfig

import os, telegram
from telegram.ext import Updater

TOKEN = "1950319109:AAGUgUsCQ-5fvHASYkQsweg5atGNw4QzXRM"
from telegram.ext import Updater
from telegram import Update


bot = Updater(TOKEN)
print(bot.bot.getChat(chat_id=332099596).status)
print(type(bot.bot.getChat(chat_id=332099596)))
print(bot.bot.getChat(chat_id=332099595))
print(type(bot.bot.getChat(chat_id=332099595)))
class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'
