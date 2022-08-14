# Generated by Django 3.2.8 on 2022-07-09 19:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BotTexts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Поиск', 'Поиск'), ('Все', 'Все'), ('МЕНЮ', 'МЕНЮ')], default='Все', help_text='Сортировка сообщений согласно местам их применения.', max_length=10)),
                ('message_code', models.CharField(default='0', help_text='Название переменной, отображается в коде', max_length=25, unique=True)),
                ('ua', models.CharField(default='0', help_text='Сообщение для UA локали, до 1000 символов, работает форматирование из Telegram. ', max_length=1000, validators=[django.core.validators.RegexValidator(code='invalid_symbol', message="0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?& символы.", regex="^[0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?&]*$")])),
                ('ru', models.CharField(default='0', help_text='Коды Emoji тут: https://www.webfx.com/tools/emoji-cheat-sheet/', max_length=1000, validators=[django.core.validators.RegexValidator(code='invalid_symbol', message="0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?& символы.", regex="^[0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?&]*$")])),
                ('en', models.CharField(default='0', help_text='{new_line} - новая строка. {другой_текст} - системная переменная. Пока лучше не трогать', max_length=1000, validators=[django.core.validators.RegexValidator(code='invalid_symbol', message="0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?& символы.", regex="^[0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?&]*$")])),
                ('raport_text', models.CharField(default='0', help_text='Что прийдет в телегу', max_length=1000, validators=[django.core.validators.RegexValidator(code='invalid_symbol', message="0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?& символы.", regex="^[0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?&]*$")])),
                ('log_text', models.CharField(default='0', help_text='Что писать в логи', max_length=1000, validators=[django.core.validators.RegexValidator(code='invalid_symbol', message="0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?& символы.", regex="^[0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ'.,-}+{ )(/:=_?&]*$")])),
            ],
            options={
                'verbose_name_plural': 'Текста бота',
            },
        ),
        migrations.CreateModel(
            name='userlevels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='NEW', help_text='Название уровня(Отображается пользователю)', max_length=20)),
                ('status', models.CharField(choices=[('ON', 'ON'), ('ADM', 'ADM'), ('OFF', 'OFF')], default='ADM', help_text='Статус уровня', max_length=20)),
                ('free_mounth', models.PositiveSmallIntegerField(default=0, help_text='Макс. поисков в календарный месяц')),
                ('free_day', models.PositiveSmallIntegerField(default=0, help_text='Макс. поисков можно использовать в день')),
                ('additional_search_price', models.DecimalField(decimal_places=2, default=0, help_text='Цена доп. поиска', max_digits=9)),
                ('pimeyes_results_count', models.PositiveSmallIntegerField(default=0, help_text='Сколько присылать результатов PY. 0 Чтобы отключить')),
                ('findclone_results_count', models.PositiveSmallIntegerField(default=0, help_text='Сколько присылать результатов FC. 0 Чтобы отключить')),
            ],
            options={
                'verbose_name_plural': 'Уровни',
            },
        ),
        migrations.CreateModel(
            name='BotSettings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('default_locale', models.CharField(choices=[('en', 'en'), ('ua', 'ua'), ('ru', 'ru')], default='en', help_text='Текста какого языка отображать пользователям. Пока меняется только глобально.', max_length=3)),
                ('maitenance', models.BooleanField(default=False, help_text='Установка статуса "Техработы" который ограничивает взаимодействие с ботом до стартового сообщения.')),
                ('show_ads', models.BooleanField(default=False, help_text='Показывать рекламу после загрузки фото')),
                ('group_requierd', models.BooleanField(default=False, help_text='Запрашивать членство в группе перед загрузкой фото. ВАЖНО!!! Бота нужно добавить в администраторы канала.')),
                ('group_name', models.CharField(default='@durov1', help_text='Имя канала на который нужно подписатсья. Формат: @durov_1123_durov. ВАЖНО!!! Бота нужно добавить в администраторы канала.', max_length=50)),
                ('support_chat_id', models.CharField(default='raport_chat_id', help_text='raport_chat_id', max_length=20)),
                ('raport_bot_key', models.CharField(default='Insert Raport key here', help_text='Raport Key', max_length=64)),
                ('raport_chat_id', models.CharField(default='raport_chat_id', help_text='raport_chat_id', max_length=20)),
                ('findclone_login', models.CharField(default='fc_login', help_text='findclone_login', max_length=20)),
                ('findclone_password', models.CharField(default='fc_password', help_text='findclone_password', max_length=20)),
                ('default_lvl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.userlevels')),
            ],
            options={
                'verbose_name_plural': 'Настройки бота',
            },
        ),
    ]