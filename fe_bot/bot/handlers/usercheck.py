from users.models import User_new
from bot.models import BotTexts, BotSettings
from tasks.models import Task
from telegram import Update
from telegram.ext import Updater
from telegram.ext import CallbackContext
from partner_program.models import BonusCode
from django.shortcuts import get_object_or_404
from django.db.models import Count
from datetime import datetime
import os

TOKEN = os.getenv("TOKEN"#, "5420343912:AAHmj752TQOLi6JdKHYygJJpnqu0WtJBEdo"
                  )


class UserValidator:
    def __init__(self, update: Update, context: CallbackContext):
        self.update = update
        self.cont = context
        self.TOKEN = TOKEN
        self.context = None
        self.check_user_reg()

    def check_user_reg(self):
        us = User_new.is_user_created(self.update, self.cont)
        self.user = us[0]
        if us[1]:
            us = self.reg_user()

    def is_user_baned(self):
        if self.user.level.name == 'BAN':
            return True

    def is_need_to_show_ads(self):
        if self.user.level.show_ads:
            return True

    def is_maitenence(self):
        maitenance = BotSettings.objects.get(pk=1).maitenance
        if maitenance:
            return True

    def is_user_have_extra_searches(self):
        if self.user.is_user_have_extra_searches():
            return False
        else:
            return True

    def is_day_limit(self):
        currentDay = datetime.now().day
        self.searches_today = Task.objects.all().filter(start_time__day=currentDay,
                                                                       chat_id=self.user.chat_id).annotate(c=Count('id'))
        self.searches_left_today = self.user.level.free_day - len(self.searches_today)
        if self.searches_left_today <= 0:
            return True

    def is_need_to_join_group(self):
        if self.user.level.group_requierd:
            try:
                self.user.bot = Updater(TOKEN)
                if self.user.bot.bot.getChatMember(str(self.user.level.group_name),
                                                       self.user.chat_id).status == 'left':
                    return True
            except Exception as e:
                print(e)

    def reg_user(self):
        if self.cont is not None and self.cont.args is not None and len(self.cont.args) > 0:
            payload = self.cont.args[0]
            if str(payload).strip() != str(self.update.message.chat_id).strip():
                try:
                    b = get_object_or_404(BonusCode, bonus_code=payload)
                    self.user.level = b.code_level
                    self.user.save()
                except Exception as e:
                    print(f'WRONG_REF: {payload}')
            self.user.ref_code = payload
        self.user.save()
