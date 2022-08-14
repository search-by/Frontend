import uuid, django, datetime
from django.db import models
from users.models import User_new


class Task(models.Model):
    FREE = 'free'
    DOP = 'dop'
    MONEY = 'money'
    TYPES = [
        (FREE, 'Бесплатная'),
        (DOP, 'Доп.'),
        (MONEY, '$'),
    ]
    id = models.AutoField(primary_key=True)
    UUID = models.UUIDField(default=uuid.uuid4, editable=False)
    file_id = models.CharField(max_length=120, default="0")
    status = models.TextField(max_length=50, default='111')
    pimeyes_status = models.SmallIntegerField(default=1)
    findclone_status = models.SmallIntegerField(default=1)
    obsh_status = models.SmallIntegerField(default=1)
    type = models.CharField(max_length=5, choices=TYPES)
    user = models.ForeignKey(User_new, on_delete=models.SET_NULL, blank=True, null=True, )
    user_lvl = models.CharField(max_length=20, default="0")
    result = models.CharField(max_length=120, default="0")
    creation_date = models.DateTimeField(blank=True, null=True, default=django.utils.timezone.now)
    last_update = models.DateTimeField(blank=True, null=True, default=django.utils.timezone.now)
    logs = models.TextField(blank=True)

    @classmethod
    def create(cls, user, UUID, file_id, type):
        logs = f'{datetime.datetime.now()} таска создана<br />'
        return cls(user=user, UUID=UUID, user_lvl=user.level, file_id=file_id, type=type, logs=logs)

    def __str__(self):
        return f'{self.status}_{self.user}_{self.UUID}'

    class Meta:
        verbose_name_plural = 'Таски'
