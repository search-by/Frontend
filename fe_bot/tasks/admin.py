import requests
from .models import Task
from django.utils.html import mark_safe
from django.contrib import admin
from rangefilter.filters import DateRangeFilter
import os

SERVER_ADRESS = os.getenv("SERVER_ADRESS", "127.0.0.1")
TOKEN = os.getenv("TOKEN", "1950319109:AAGUgUsCQ-5fvHASYkQsweg5atGNw4QzXRM")


class TaskAdmin(admin.ModelAdmin):
    fields = ('user', 'status', 'pimeyes_status', 'last_update', 'user_lvl', 'result', 'type', 'creation_date',  'file', 'logs',)
    readonly_fields = ('user', 'last_update', 'pimeyes_status', 'type', 'result', 'creation_date', 'file', 'logs', 'user_lvl')
    list_display = ('last_update', 'user_id', 'pimeyes_status', 'status', 'result', )
    list_display_links = ('user_id', 'last_update', )
    list_filter = ('status', ('creation_date', DateRangeFilter), 'pimeyes_status', 'user_lvl')

    @admin.display
    def user_id(self, obj):
        if not obj.user:
            chat_id = '-'
        else:
            chat_id = obj.user.chat_id
        return mark_safe(f'<a href="/admin/users/user_new/{chat_id}/change/">{chat_id}</a>')

    @admin.display
    def file(self, obj):
        file_id = obj.file_id
        try:
            response = requests.get(f'https://api.telegram.org/bot{TOKEN}/getfile?file_id={file_id}')
            if response.status_code != 200:
                raise Exception
            file_path = response.json()["result"]["file_path"]
            return mark_safe(f'<input type="text" name="status" value="{file_id}" class="vTextField" maxlength="10">'
                             f'<br/><br/><img width="400" src="https://api.telegram.org/file/bot{TOKEN}/{file_path}"/><br/><p>/UUID895634534567565 {obj.UUID}</p>')
        except Exception as e:
            return mark_safe(
                '<input type="text" name="status" value="{file_id}" class="vTextField" maxlength="10">'
                '<br /><br /><a href="https://api.telegram.org/bot{TOKEN}/getfile?file_id={file_id}">{file_id}</a>'
                '<br /><br /> <p>{e}</p><p>/UUID895634534567565 {UUID}</p>'.format(
                    TOKEN=TOKEN,
                    file_id=file_id,
                    e=e,
                    UUID=obj.UUID
                ))
    user_id.short_description = 'Пользователь'


admin.site.register(Task, TaskAdmin)