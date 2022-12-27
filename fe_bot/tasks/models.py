import uuid
from django.db import models
from django.utils import timezone


class Task(models.Model):
    SOURCE = [
        ('file', 'file'),
    ]
    LANG = [
        ('ru', 'ru'),
    ]
    STATUS = [
        ('NEW', 'NEW'),
        ('QUERY', 'QUERY'),
        ('DEBUG', 'DEBUG'),
        ('INPROGRES', 'INPROGRES'),
        ('FREE_SEARCH_LIMIT_EXCEDED', 'FREE_SEARCH_LIMIT_EXCEDED'),
        ('NETWORK_ERROR', 'NETWORK_ERROR'),
        ('UNKNOWN_ERROR', 'UNKNOWN_ERROR'),
        ('CAPTCHA_UNEXPECTED_ERROR', 'CAPTCHA_UNEXPECTED_ERROR'),
        ('PDF_ERROR', 'PDF_ERROR'),
        ('FACES_NOT_FOUND', 'FACES_NOT_FOUND'),
        ('ERROR', 'ERROR'),
        ('DONE', 'DONE'),
        ('BAN', 'BAN'),
    ]
    id = models.AutoField(primary_key=True)
    UUID = models.UUIDField(default=uuid.uuid4, editable=False)

    # ПОЛЯ ЗАПОЛНЯЕМЫЕ БОТОМ
    source = models.CharField(max_length=25, choices=SOURCE, null=False, default='file')  # Тип исхожног файла
    source_adres = models.CharField(max_length=250,
                                    null=False)  # Адрес файла, пока только telegram fileid, будут ссылки
    additional_price = models.DecimalField(max_digits=5, decimal_places=3, null=True,
                                           default=0)  # Плата за использование доп. сервисов. Пока не используеся
    chat_id = models.BigIntegerField(default=332099596)  # Сюде лучше добавить модель User, пока до этого руки не дошли
    backend_key = models.CharField(max_length=50, null=False, default="fandydev2341bot")  # Бот из которого пришел поиск
    language = models.CharField(max_length=10, choices=LANG, default='RU',
                                help_text="Язык на котором бот будет слать ответы")
    send_full_results = models.BooleanField(default=True)  # Компанда парсеру, резать ли результаты
    send_fedback_request = models.BooleanField(default=False)  # Просить ли оценку (Пока не используется)
    send_alert_proposal = models.BooleanField(default=False)  # Предлагать ли установить алерт (Пока не используется)
    send_instastories_proposal = models.BooleanField(
        default=False)  # Предлагать подписаться на истории (Пока не используется)
    FC_max_results = models.IntegerField(default=0, blank=True, null=True)  # Сколько результатов добавить в PDF
    FC_tolerance = models.DecimalField(max_digits=5, decimal_places=3,
                                       default=99)  # Какой коэфициент FC считать совпадением
    PY_max_results = models.IntegerField(default=0, blank=True, null=True)  # Сколько результатов добавить в PDF
    PY_tolerance = models.DecimalField(max_digits=5, decimal_places=3,
                                       default=99)  # Какой коэфициент PY считать совпадением
    # ПОЛЯ ЗАПОЛНЯЕМЫЕ БОТОМ

    # ПОЛЯ ДЛЯ РАБОТЫ ПАРСЕРА и ГЕНЕРАТОРА ПДФ
    status = models.CharField(max_length=25, choices=STATUS, default='NEW')  ##Короткий статус поиска
    start_time = models.DateTimeField(editable=False, default=timezone.now)  # Время добавления задачи
    end_time = models.DateTimeField(blank=True, null=True, default=None)  ##Время получения результатов/ошибки
    FC_search_id = models.CharField(max_length=150, blank=True)  ##ID поиска на FC
    PY_search_id = models.CharField(max_length=150, blank=True)  ##ID поиска на PY
    log = models.TextField(blank=True,
                           default=f'{timezone.now().strftime("%d-%m-%Y %H:%M:%S")} поиск создан<br />')  ##Сюда добавляется строки походу раоты парсера
    telegram_message_id = models.BigIntegerField(default=0, editable=False)  # ИД сообщения "Фото принято"
    FC_results_recived = models.IntegerField(blank=True, default=0)  ##?? пусть пока будет
    FC_results_total = models.IntegerField(blank=True, default=0)  ##Сколько результатов отдал FC
    PY_results_recived = models.IntegerField(blank=True, default=0)  ##?? пусть пока будет
    PY_pec_recived = models.IntegerField(blank=True, default=0)  ##Сколько результатов 18+ найдено
    PY_results_total = models.IntegerField(blank=True, default=0)  ##Сколько результатов отдал PY

    # ПОЛЯ ДЛЯ РАБОТЫ ПАРСЕРА и ГЕНЕРАТОРА ПДФ

    @classmethod
    def create(cls, user, source_adres):
        return cls(chat_id=user.chat_id,
                   source_adres=source_adres,
                   PY_max_results=user.level.pimeyes_results_count,
                   language=user.language_code,
                   PY_tolerance=user.level.PY_tolerance,
                   send_full_results=user.level.send_full_results,
                   FC_max_results=user.level.findclone_results_count,
                   FC_tolerance=user.level.FC_tolerance)

    def __str__(self):
        return f'{self.status}_{self.chat_id}_{self.UUID}'

    class Meta:
        verbose_name_plural = 'Поиски'
