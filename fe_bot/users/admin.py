from django.contrib import admin
from django.utils.html import mark_safe
from .models import Logs, User_new
from rangefilter.filters import DateRangeFilter
from tasks.models import Task
import os

BOT_NAME = os.getenv("BOT_NAME", default="fandydev2341bot")
TOKEN = os.getenv("TOKEN", default="1950319109:AAGUgUsCQ-5fvHASYkQsweg5atGNw4QzXRM")
SERVER_ADRESS = os.getenv("SERVER_ADRESS", default="127.0.0.1")


class LogsAdmin(admin.ModelAdmin):
    search_fields = ('chat_id',)
    list_display = ('date_added', 'chat_id', 'text',)
    list_display_links = ('chat_id', )
    list_filter = (('date_added', DateRangeFilter), )


class UserNewAdmin(admin.ModelAdmin):
    fields = ('profile_fotos', 'name', 'ban_status', 'referer_link', 'language_code', 'total_searches',
    'level',  'user_logs', 'reg_date', 'balance', 'extraSearches', 'coment', )
    readonly_fields = ('profile_fotos', 'name', 'ban_status', 'referer_link', 'reg_date',
                       'total_searches',
                       'user_logs')
    search_fields = ('username', 'first_name', 'last_name',  'chat_id', )
    list_display = ('reg_date', 'chat_id', 'total_searches_1',
                    'ref_code', '__str__')
    list_display_links = ('chat_id', 'ref_code')
    list_filter = (('reg_date', DateRangeFilter), 'level', 'ref_code',)

    @admin.display
    def ban_status(self, obj):
        status = obj.is_bot_active()
        if status[0]:
            ban_status = f'БОТ {BOT_NAME} АКТИВЕН! Последняя проверка: {status[1]}'
        else:
            ban_status = f'<h4 style="color:Tomato;">БОТ {BOT_NAME} НЕ АКТИВЕН У ПОЛЬЗОВАТЕЛЯ! </h4>  Последняя проверка: {status[0]} <br />'
        return mark_safe(
            '<b>{ban_status}</b><br />'.format(
                ban_status=ban_status
            ))

    @admin.display
    def profile_fotos(self, obj):
        fotos_array = obj.get_profile_fotos()
        gallery = '<br />'
        if fotos_array[0]:
            for count, item in enumerate(fotos_array[1]["photos"]):
                if count in (5, 10, 15, 20):
                    gallery += '<br />'
                gallery += f'<img width="160" src="{item}"/>'
        else:
            gallery += f'<h5>Нет фото, или бот {BOT_NAME} не активен у пользователя</h5>'
        return mark_safe(gallery)

    @admin.display
    def name(self, obj):
        return mark_safe(
            '<b><a href="https://t.me/{username}">{username}</a></b><br /><br />'
            '<b>{first_name}<br />{last_name}</b>'.format(
                username=obj.username,
                first_name=obj.first_name,
                last_name=obj.last_name,
            ))

    @admin.display
    def total_searches(self, obj):
        total_searches_count = Task.objects.all().filter(chat_id=obj.chat_id)
        return mark_safe('<a href="/{link}={chat_id}">Всего поисков: {total_searches_count} </a>'.format(
            bot_url=SERVER_ADRESS,
            link='admin/tasks/task/?user_id__chat_id__exact',
            chat_id=obj.chat_id,
            total_searches_count=total_searches_count,
        ))

    @admin.display
    def total_searches_1(self, obj):
        total_searches_count = Task.objects.all().filter(chat_id=obj.chat_id)
        return mark_safe('<a href="/{link}={chat_id}">Поисков: {total_searches_count} </a><br /><br />'.format(
            bot_url=SERVER_ADRESS,
            link='admin/tasks/task/?user_id__chat_id__exact',
            link_unfinished='admin/tasks/task/?pimeyes_status__gt=1&pimeyes_status__lt=9&user_id__chat_id__exact',
            link_finished='admin/tasks/task/?pimeyes_status=9&user_id__chat_id__exact',
            chat_id=obj.chat_id,
            total_searches_count=total_searches_count,
            errorlink='admin/tasks/task/?q',
        ))

    @admin.display
    def user_logs(self, obj):
        logs = Logs.objects.filter(chat_id=obj.chat_id).order_by('-date_added')[:50]
        log_text = " "
        for item in logs:
            log_text += item.text + '<br />'
        return mark_safe('<a href="/admin/users/logs/?q={chat_id}">Все логи</a><br /><br />'
                         '<b>Последние 50 действий:</b> <br /><br />{log_text}'.format(
            log_text=log_text,
            chat_id=obj.chat_id,
        ))

    @admin.display
    def referer_link(self, obj):
        return mark_safe('<a href="/admin/partner_program/bonuscode/?bonus_code={}">Код приглашения: {}</a>'.format(
            obj.ref_code,
            obj.ref_code
        ))
admin.site.register(Logs)
admin.site.register(User_new)
#admin.site.register(Logs, LogsAdmin)
#admin.site.register(User_new, UserNewAdmin)
