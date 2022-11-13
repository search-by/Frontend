from __future__ import annotations
from django.utils.timezone import now
from typing import Union, Optional, Tuple
from telegram import Update
from typing import Dict
from datetime import datetime
from bot.models import userlevels, BotSettings
from partner_program.models import BonusCode
from django.db.models import Count, DateField
from django.db import models
from django.shortcuts import get_object_or_404
import datetime
import django
import os
from telegram.ext import Updater
from telegram import Chat
import telegram
import requests

TOKEN = os.getenv("TOKEN")

PARSE_MODE = os.getenv("PARSE_MODE", "MarkdownV2")
LOCALE = os.getenv("LOCALE", "ua")
LOCATION = os.getenv("LOCATION", "/home/beadmin/files")
BOT_NAME = os.getenv("BOT_NAME", "fandydev2341bot")
TOKEN_RAPORT = os.getenv("TOKEN_RAPORT", "1979319236:AAH33slvXbRE94Aj1G8CAd0m35Ao7Dtq2XE")

nb = dict(null=True, blank=True)


def extract_user_data_from_update(update: Update) -> Dict:
    if update.message is not None:
        user = update.message.from_user.to_dict()
    elif update.inline_query is not None:
        user = update.inline_query.from_user.to_dict()
    elif update.chosen_inline_result is not None:
        user = update.chosen_inline_result.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.from_user is not None:
        user = update.callback_query.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.message is not None:
        user = update.callback_query.message.chat.to_dict()
    else:
        raise Exception(f"Can't extract user data from update: {update}")
    return dict(
        chat_id=user["id"],
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name", "language_code"]
            if k in user and user[k] is not None
        },
    )


class CreateTracker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class CreateUpdateTracker(CreateTracker):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(CreateTracker.Meta):
        abstract = True


class User_new(CreateUpdateTracker):
    chat_id = models.BigIntegerField(primary_key=True, unique=True)
    username = models.CharField(max_length=32, **nb)
    first_name = models.CharField(max_length=512)
    last_name = models.CharField(max_length=512, **nb)
    language_code = models.CharField(max_length=8, help_text="Язык клиента взятый из профиля", **nb)
    ref_code = models.CharField(max_length=64, **nb)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    level = models.ForeignKey(userlevels, on_delete=models.SET_NULL, default=1, null=True)
    extraSearches = models.BigIntegerField(default=0)
    reg_date = models.DateField(default=django.utils.timezone.now)
    coment = models.CharField(max_length=2512, blank=True)

    def is_bot_active(self) -> (Tuple[bool, DateField, Chat] or Tuple[bool, DateField, None]):
        bot = Updater(TOKEN)
        date = django.utils.timezone.now().strftime("%d-%m-%Y %H:%M")
        try:
            chat = bot.bot.getChat(chat_id=self.chat_id)
            return True, date, chat
        except telegram.error.BadRequest:
            return False, date, None

    def get_profile_fotos(self, size=0, limmit=20) -> Tuple[bool, Dict]:
        photos = {"total_count": 0,
                  "date": datetime.datetime.now().strftime("%d-%m-%Y %H:%M"),
                  "photos": []}
        try:
            profile_photos = \
            requests.get(f'https://api.telegram.org/bot{TOKEN}/getUserProfilePhotos?user_id={self.chat_id}').json()['result']
            photos["total_count"] = int(profile_photos["total_count"])
            if photos["total_count"] == 0:
                return True, photos
        except Exception as e:
            print(e)
            return False, photos
        for count, foto_array in enumerate(profile_photos["photos"]):
            if count >= limmit:
                return True, photos
            try:
                files_request = requests.get(
                    f'https://api.telegram.org/bot{TOKEN}/getfile?file_id={foto_array[size]["file_id"]}')
                file_path = files_request.json()['result']['file_path']
                photos['photos'].append(f'https://api.telegram.org/file/bot{TOKEN}/{file_path}')
            except Exception as e:
                pass
        return True, photos

    @classmethod
    def is_user_created(cls, update: Update, context) -> Tuple[User_new, bool]:
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(chat_id=data["chat_id"], defaults=data)
        return u, created

    @classmethod
    def get_user_and_created(cls, update: Update, context) -> Tuple[User_new, bool]:
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(chat_id=data["chat_id"], defaults=data)
        if created:
            u.change_user_level(u, new=True)
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["chat_id"]).strip():
                    u.ref_code = payload
                    u.change_user_level(u, payload)
                    u.save()
                    try:
                        b = get_object_or_404(BonusCode, bonus_code=payload, type='Авто')
                        referer = User_new.objects.get(chat_id=int(b.bonus_code))
                        u.change_free_searches(referer, 1, referer.chat_id)
                    except Exception as e:
                        print(e)
            u.create_self_auto_bonus_code(u)
        return u, created

    @classmethod
    def get_user(cls, update: Update, context):
        u, _ = cls.get_user_and_created(update, context)
        if u.level == None:
            u.change_user_level(u, new=True)
        ban_and_m_result = cls.check_ban_and_maitenance(u)
        search_type = cls.get_search_type(u)
        total_refs = cls.objects.all().filter(ref_code=u.chat_id)
        return {"user": u,
                'status': ban_and_m_result,
                "is_allowed": ban_and_m_result[0],
                "allowed_status": ban_and_m_result[1],
                "search_type": search_type,
                "total_refs": len(total_refs)}

    @classmethod
    def get_search_type(cls, u: User_new):
        u.count_of_searches()
        if u.searches['searches_left_today'] > 0 and u.searches['searches_left_this_mounth'] > 0:
            return 'free'
        if u.extraSearches > 0:
            return 'dop'
        if u.balance >= u.level.additional_search_price:
            return 'money'
        else:
            return False

    @classmethod
    def check_ban_and_maitenance(cls, u: User_new):
        settings = BotSettings.objects.get(id=1)
        return [True, 'STATUS_OK']

    @classmethod
    def get_user_by_username_or_user_id(cls, username_or_user_id: Union[str, int]) -> Optional[User_new]:
        username = str(username_or_user_id).replace("@", "").strip().lower()
        if username.isdigit():
            return cls.objects.filter(chat_id=int(username)).first()
        return cls.objects.filter(username__iexact=username).first()

    @classmethod
    def change_user_level(cls, u: User_new, level=None, new=False) -> Optional[User_new]:
        default_lvl = BotSettings.objects.get(pk=1).default_lvl
        if u.level is None:
            u.level = default_lvl
        if level:
            try:
                level = int(level)
                u.level = userlevels.objects.get(pk=1)
            except ValueError:
                u.level = userlevels.objects.get(name=level)
        elif new:
            u.level = default_lvl
            u.save()
        return u

    def is_user_have_extra_searches(self):
        extraSearches = int(self.extraSearches)
        if extraSearches > 0:
            self.extraSearches -= 1
            self.save()
            return True
        else:
            return False

    def get_search_type(self):
        self.count_of_searches()
        if self.searches['searches_left_today'] > 0 and self.searches['searches_left_this_mounth'] > 0:
            return 'free'
        if self.extraSearches > 0:
            return 'dop'
        if self.balance >= self.level.additional_search_price:
            return 'money'
        else:
            return False

    '''
    def pay(self, amount):
        try:
            amount = float(amount)
        except Exception:
            message = 'Вводите только цифры'
            return False
        d = Decimal.from_float(amount)
        if self.balance < abs(d):
            message = 'Недостаточно денег на балансе.'
            return False
        self.balance -= abs(d)
        self.save()
        message = f'{abs(d)}$ снято с баланса'
        return True

    # @classmethod
    def addbalance(self, amount):
        try:
            amount = float(amount)
        except Exception:
            message = 'Вводите только цифры'
            return message
        d = Decimal.from_float(amount)
        if d < 1:
            message = 'Min платеж 1$'
            return message
        if d > 101:
            message = 'Max платеж 99.99$'
            return message
        self.balance += d
        try:
            self.save()
            message = f'Зачислено: {d}$'
        except Exception:
            message = f'...'
            self.balance -= d
        return message
    
    @classmethod
    def is_user_have_free_searches(cls, update: Update, context):
        u, _ = cls.get_user_and_created(update, context)
        currentMonth = datetime.datetime.now().month
        currentDay = datetime.datetime.now().day
        cls.all_searches = u.task_set.all().annotate(c=Count('id'))
        cls.searches_this_mounth = cls.all_searches.filter(creation_date__month=currentMonth).annotate(c=Count('id'))
        cls.searches_today = cls.all_searches.filter(creation_date__day=currentDay, type='free').annotate(c=Count('id'))
        now = datetime.datetime.today()
        tomorrow = now + datetime.timedelta(days=1)
        next_month = now + relativedelta.relativedelta(months=1, day=1, hour=0, minute=0, second=0)
        cls.searches_left_today = u.level.free_day - cls.searches_today.count()
        cls.searches_left_mounth = u.level.free_mounth - cls.searches_this_mounth.count()
        if cls.searches_left_mounth <= 0:
            time_till_new_search_raw = datetime.datetime.combine(next_month, datetime.time.min) - now
            cls.time_till_new_search = str(time_till_new_search_raw.days)
            return False
        elif cls.searches_left_today <= 0:
            time_till_new_search = datetime.datetime.combine(tomorrow, datetime.time.min) - now
            cls.time_till_new_search = ':'.join(str(time_till_new_search).split(':')[:2])
            return False
        else:
            cls.time_till_new_search = '0'
            return True

    @classmethod
    def is_user_have_extra_searches(cls, update: Update, context):
        u, _ = cls.get_user_and_created(update, context)
        extraSearches = int(u.extraSearches)
        if extraSearches > 0:
            u.extraSearches -= 1
            u.save()
            return True
        else:
            return False

    @classmethod
    def is_user_have_limited_promo(cls, update: Update, context) -> bool:
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(chat_id=data["chat_id"], defaults=data)
        if u.level.searches_max > 0:
            all_searches = u.task_set.all().annotate(c=Count('id'))
            if len(all_searches) > u.level.searches_max:
                return True
            else:
                return False
        return False

    @classmethod
    def is_user_in_the_group(cls, update: Update, context) -> bool:
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(chat_id=data["chat_id"], defaults=data)

        if u.level.group_requierd:
            try:
                u.bot = Updater(TOKEN)
                if u.bot.bot.getChatMember(str(u.level.group_name), u.chat_id):
                    return True
                else:
                    return False
            except Exception as e:
                return False

    def is_user_in_group(self):
        return True
        if self.level.group_requierd:
            try:
                self.bot = Updater(TOKEN)
                if self.bot.bot.getChatMember(str(self.level.group_name), self.chat_id):
                    return True
                else:
                    return False
            except Exception as e:
                return False

    @classmethod
    def is_user_baned(cls, update: Update, context) -> bool:
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(chat_id=data["chat_id"], defaults=data)
        if u.level.name == 'BAN':
            return True
        else:
            return False

    @classmethod
    def create_self_auto_bonus_code(self, u):
        b = BonusCode()
        b.type = 'Авто'
        b.bonus_code = u.chat_id
        b.code_owner = u
        b.code_creator = u
        try:
            b.save()
            return b
        except Exception:
            pass
    '''
    #@classmethod
    def count_of_searches(self):
        currentMonth = datetime.datetime.now().month
        currentDay = datetime.datetime.now().day
        all_searches = self.task_set.all()
        searches_total = all_searches.annotate(c=Count('id'))
        searches_this_mounth = all_searches.filter(creation_date__month=currentMonth).annotate(c=Count('id'))
        searches_today = all_searches.filter(creation_date__day=currentDay, type='free').annotate(c=Count('id'))
        self.searches = {
            'searches_total': len(searches_total),
            'searches_this_mounth': len(searches_this_mounth),
            'searches_today': len(searches_today),
            'searches_left_today': self.level.free_day - len(searches_today),
            'searches_left_this_mounth': self.level.free_mounth - len(searches_this_mounth)
        }

    def __str__(self):
        return f'{self.chat_id}_{self.language_code}_{self.first_name}_{self.level}'

    class Meta:
        verbose_name_plural = 'Пользователи'


class Logs(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    chat_id = models.BigIntegerField(default=0)
    user_name = models.CharField(max_length=150, default="-")
    text = models.CharField(max_length=2000, default="-")

    class Meta:
        verbose_name_plural = 'История'

    def __str__(self):
        return str(f"{self.date_added.strftime('%D %H:%M:%S')}  {self.user_name}: {self.text}")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
