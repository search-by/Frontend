import django
from django.db import models


class BonusCode(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    id = models.AutoField(primary_key=True)
    creation_date = models.DateTimeField(default=django.utils.timezone.now, editable=False)
    bonus_code = models.CharField(max_length=15, unique=True, blank=False)
    code_level = models.ForeignKey("bot.userlevels", on_delete=models.CASCADE, related_name='userlevels',
                                   help_text="Уровень который получит пользователь зарегавшийся по коду")
    coment = models.TextField(blank=True, null=True,
                              help_text="Поле для заметок. На работу не влияет.")

    def __str__(self):
        return f'{self.bonus_code}'

    class Meta:
        verbose_name_plural = 'Бонус-коды'
