from django.contrib import admin
from .models import BotSettings, userlevels, BotTexts
from django.forms import TextInput
from django.db import models


class SettingsAdmin(admin.ModelAdmin):
    actions = None
    fields = ('default_locale', 'default_lvl', 'maitenance', 'raport_bot_key', "findclone_login",
              "findclone_password", "pimeyes_login", "pimeyes_password")


class TextsAdmin(admin.ModelAdmin):
    actions = None
    fields = ('message_code', 'en', 'ru',  "raport_text", "log_text")
    list_display = ('message_code', 'ru', 'en')
    list_display_links = ('message_code', )
    list_editable = ('en', 'ru', )
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '70'})},
    }


class LevelAdmin(admin.ModelAdmin):
    fields = ('name',  'free_day', 'pimeyes_results_count', 'PY_tolerance', "findclone_results_count", 'FC_tolerance',
              "show_ads", "send_full_results", "group_requierd", "group_name", "coment",)
    list_display = ('name', "show_ads", "send_full_results", "group_requierd",
                    'free_day', 'pimeyes_results_count', "findclone_results_count",)
    list_display_links = ('name', )


admin.site.register(BotTexts, TextsAdmin)
admin.site.register(userlevels, LevelAdmin)
admin.site.register(BotSettings, SettingsAdmin)