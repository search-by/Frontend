#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, telegram
from telegram.ext import Updater
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from users.models import User_new
from users.models import Logs
import emoji
from bot.models import BotTexts, BotSettings
from telegram import KeyboardButton


TOKEN = os.getenv("TOKEN", "1950319109:AAGUgUsCQ-5fvHASYkQsweg5atGNw4QzXRM")
PARSE_MODE = os.getenv("PARSE_MODE", "MarkdownV2")
LOCALE = os.getenv("LOCALE", "ua")
LOCATION = os.getenv("LOCATION", "/home/beadmin/files")
BOT_NAME = os.getenv("BOT_NAME", "fandydev2341bot")
TOKEN_RAPORT = os.getenv("TOKEN_RAPORT", "1979319236:AAH33slvXbRE94Aj1G8CAd0m35Ao7Dtq2XE")


FIRST, SECONT, THIRD, FOURTH, PROPOSAL1, PROPOSAL2, PLATEGKA1, PLATEGKA2, LIQPAY = range(9)


class Message:
    def __init__(self, status, update=None, log=False, raport='0', context: CallbackContext = None, chat_id=None, var=None, user=None):
        self.locale = BotSettings.objects.get(pk=1).default_locale
        self.bot = Updater(TOKEN)
        self.status = status
        self.user = User_new.objects.all().filter(chat_id=update.message.chat.id)[0]
        self.BOT_NAME = BOT_NAME.replace('_', '\_')
        self.texts = {}
        self.raw_texts = BotTexts.objects.all().filter(message_code=self.status)
        self.chat_id = update.message.chat.id
        self.menu_text_profile = BotTexts.objects.all().filter(message_code='MENU_TEXT_PROFILE')
        self.menu_text_home = BotTexts.objects.all().filter(message_code='BUTTON_HOME')

        for big_item in self.raw_texts:
            cleaned_text = emoji.emojize(self.insert_vars(big_item.txt(self.locale)),
                                         use_aliases=True).replace(".", "\.").replace("-", "\-").replace("=", "\=").replace("'", "\'").replace("_", "\_")
            cleaned_logs = emoji.emojize(self.insert_vars(big_item.log_text),
                                         use_aliases=True).replace(".", "\.").replace("-", "\-").replace("=","\=").replace("'", "\'").replace("_", "\_")
            cleaned_raports = emoji.emojize(self.insert_vars(big_item.raport_text),
                                         use_aliases=True).replace(".", "\.").replace("-", "\-").replace("=","\=").replace("'", "\'").replace("_", "\_")
            self.texts[big_item.message_code] = {'text' : cleaned_text,
                     'log_text' : cleaned_logs,
                     'raport_text' : cleaned_raports}

        reply_keyboard_first = [
            [KeyboardButton('Домой'),
             KeyboardButton('Профиль')
             ]]
        self.reply_markup = ReplyKeyboardMarkup(reply_keyboard_first, selective=True, resize_keyboard=True)

        if log: self.write_logs(log)
        if raport: self.send_raport(raport)

    def insert_vars(self, text, light=False):
        BOT_NAME = self.BOT_NAME.replace("_", "\_")

        new_text = text.format(chat_id=self.chat_id,
                         level=self.user.level,
                         group=self.user.level.group_name,
                         ref_link="1",#f"https://t.me/{BOT_NAME}?start={self.user.chat_id}",
                         #ref_count=self.user["total_refs"],
                         balance=str(self.user.balance),
                         searches_left_today="1",#self.user.get_user_searches_left(self.user),
                         extra_searches="1",#self.user.extraSearches,
                         new_line='\n',
                         #time_till_new_search=self.var,
                         #group=self.group,
                         time="1",#datetime.datetime.now().strftime("%d/%m/%y %H:%M")
                               )
        return new_text

    def write_logs(self, log):
        custom_text = "_"
        if self.texts[self.status]["log_text"] != '0':
            if log:
                custom_text = log
            text_to_write = f'{self.texts[self.status]["log_text"]} {custom_text}'
            l = Logs(chat_id=self.chat_id, text=f'{text_to_write}')
            l.save()

    def send_raport(self, raport):
        if raport != '0':
            self.raport_bot.bot.send_message(self.raport_chat_id, f"{self.texts[self.status]['raport_text']} {raport}",#
                                             parse_mode=PARSE_MODE, disable_web_page_preview=True)

    def send_typing(self):
        self.bot.bot.send_chat_action(self.update.message.chat.id, action=telegram.ChatAction.TYPING)

    def message_by_status(self, no_first=False):
        self.bot.bot.send_message(self.chat_id,
                                  text=self.texts[self.status]['text'],
                                  parse_mode=PARSE_MODE,
                                  reply_markup=self.reply_markup
                                  )
        return FIRST

    def send_message(self):
        self.bot.bot.send_message(self.chat_id,
                                  text=self.texts[self.status]['text'],
                                  parse_mode=PARSE_MODE,
                                  reply_markup=self.reply_markup
                                  )
        
    def profile(self, update: Update, context: CallbackContext) -> None:
        self.bot.bot.send_message(self.chat_id, self.texts[self.status]['text'],
                                  parse_mode=PARSE_MODE, reply_markup=self.reply_markup)

    def inline(self) -> None:
        self.bot.bot.send_message(self.chat_id, self.texts[self.status]['text'], parse_mode=PARSE_MODE, disable_web_page_preview=True)

    def start(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(self.texts[self.status]['text'], parse_mode=PARSE_MODE, reply_markup=self.reply_markup)

    def __getitem__(self):
        return ['is_allowed']
