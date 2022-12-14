# coding: utf-8
from django.db import models
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(regex='^[0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ\'.,-}+{ )(/:=_?&]*$',
                              message='0-9a-zA-ZА-Яа-яёЁЇїІіЄєҐґ\'.,-}+{ )(/:=_?& символы.', code='invalid_symbol')


class BotTexts(models.Model):
    message_code = models.CharField(max_length=200, default='0', help_text="Название переменной, отображается в коде", unique=True)
    ua = models.CharField(max_length=1000, default='0', help_text="Сообщение для UA локали, до 1000 символов, работает форматирование из Telegram. ", validators=[alphanumeric])
    ru = models.CharField(max_length=1000, default='0', help_text="Коды Emoji тут: https://www.webfx.com/tools/emoji-cheat-sheet/", validators=[alphanumeric])
    en = models.CharField(max_length=1000, default='0', help_text="{new_line} - новая строка. {другой_текст} - системная переменная. Пока лучше не трогать", validators=[alphanumeric])
    raport_text = models.CharField(max_length=1000, default='0', help_text="Что прийдет в телегу", validators=[alphanumeric])
    log_text = models.CharField(max_length=1000, default='0', help_text="Что писать в логи", validators=[alphanumeric])

    def txt(self, locale=None):
        for attribute, value in self.__dict__.items():
            if attribute == locale:
                return value

    def __str__(self):
        return 'Код: {:_<15} ___ UA: {}... ___ EN:  {}... ___ RU: {}'.format(self.message_code, self.ua[:10],self.en[:10], self.ru)

    class Meta:
        verbose_name_plural = 'Текста бота'


class TelegramPaymentLog(models.Model):
    telegram_id = models.CharField("Telegram id", max_length=255)
    amount = models.FloatField("Сумма", default=0)
    currency = models.CharField("Валюта", max_length=255)

    STATUS_CHOICES = (
        ("waiting", "В ожидании оплаты"),
        ("payed", "Оплачено"),
    )
    status = models.CharField("Статус", choices=STATUS_CHOICES, default="waiting", max_length=15)
    created = models.DateTimeField("Дата создания", auto_now_add=True)

    def __str__(self):
        return f"Платеж №{self.id} от пользователя {self.telegram_id}"

    class Meta:
        verbose_name = 'Логи оплат'
        verbose_name_plural = verbose_name


class userlevels(models.Model):
    name = models.CharField(max_length=200, default="NEW", help_text="Название уровня(Отображается пользователю)")
    free_day = models.PositiveSmallIntegerField(default=0, help_text="Макс. поисков можно использовать в день")
    pimeyes_results_count = models.PositiveSmallIntegerField(default=0,
                                                             help_text="Сколько присылать результатов PY. "
                                                                       "0 Чтобы отключить")
    PY_tolerance = models.DecimalField(max_digits=16, decimal_places=14, default=99.99)
    findclone_results_count = models.PositiveSmallIntegerField(default=0,
                                                             help_text="Сколько присылать результатов FC. "
                                                                       "0 Чтобы отключить")
    FC_tolerance = models.DecimalField(max_digits=5, decimal_places=3, default=99.99)
    show_ads = models.BooleanField(default=False, help_text="Показывать рекламу после загрузки фото")
    send_full_results = models.BooleanField(default=False)
    group_requierd = models.BooleanField(default=False,
                                         help_text="Запрашивать членство в группе перед загрузкой фото. ВАЖНО!!! "
                                                   "Бота нужно добавить в администраторы канала.")
    group_name = models.CharField(default='@search_by_face_channel', max_length=50,
                                  help_text="Имя канала на который нужно подписатсья. Формат: @durov_1123_durov. "
                                            "ВАЖНО!!! "
                                            "Бота нужно добавить в администраторы канала.")
    coment = models.TextField(blank=True, null=True,
                              help_text="Поле для заметок. На работу не влияет.")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Уровни'


class BotSettings(models.Model):
    LANGS = [
        ('en', 'en'),
        ('ua', 'ua'),
        ('ru', 'ru'),
    ]

    id = models.AutoField(primary_key=True)
    default_locale = models.CharField(choices=LANGS, default='en', max_length=3,
                                      help_text="Текста какого языка отображать пользователям. Пока меняется только глобально.")
    default_lvl = models.ForeignKey(userlevels, on_delete=models.CASCADE, blank=False, default=1,
                                    help_text="Уровень который будет присвоен пользователю пришедшему без Ref. кода")
    maitenance = models.BooleanField(default=False, help_text="Установка статуса \"Техработы\" который ограничивает "
                                                              "взаимодействие с ботом до стартового сообщения.")
    support_chat_id = models.CharField(default='raport_chat_id', max_length=20, help_text="raport_chat_id")
    raport_bot_key = models.CharField(default='Insert Raport key here', max_length=64, help_text="Ключь бота для рапортов")
    raport_chat_id = models.CharField(default='raport_chat_id', max_length=20, help_text="ИД чата для отправки сообщений об ошибках")
    findclone_login = models.CharField(default='fc_login', max_length=20, help_text="Номер для Findclone, вводить с + ")
    findclone_password = models.CharField(default='fc_password', max_length=20, help_text="Пароль Findclone")
    pimeyes_login = models.CharField(default='fc_login', max_length=40, help_text="Email аккаунта Pimeyes")
    pimeyes_password = models.CharField(default='fc_password', max_length=40, help_text="Пароль для аккаунта Pimeyes")

    def __str__(self):
        return 'Базовые настройки'

    class Meta:
        verbose_name_plural = 'Настройки бота'

