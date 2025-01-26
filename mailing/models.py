from django.db import models

from users.models import CustomUser


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите email")
    fio = models.CharField(max_length=150, verbose_name="ФИО", help_text="Укажите свои фамилию, имя и отчество")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    owner = models.ForeignKey(CustomUser, verbose_name="Автор", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["fio"]


class Message(models.Model):
    subject = models.CharField(max_length=350, verbose_name="Тема письма")
    body = models.TextField(blank=True, null=True, help_text="Введите текст сообщения")
    owner = models.ForeignKey(CustomUser, verbose_name="Автор", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Newsletter(models.Model):
    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена'),
    ]

    start_sent_at = models.DateTimeField(verbose_name='Дата и время первой отправки')
    finish_sent_at = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name='Статус рассылки'
    )
    message = models.ForeignKey(Message, blank=True, null=True, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(Subscriber, related_name='newsletter_subscribers')
    owner = models.ForeignKey(CustomUser, verbose_name="Автор", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f' Рассылка id {self.pk}'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"


class AttemptSent(models.Model):
    SUCCESSFUL = 'Успешно'
    NOT_SUCCESSFUL = 'Не успешно'

    STATUS_CHOICES = [
        (SUCCESSFUL, 'Успешно'),
        (NOT_SUCCESSFUL, 'Не успешно'),

    ]

    created_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )
    server_response = models.TextField(verbose_name="Ответ почтового сервера")
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, verbose_name="Автор", blank=True, null=True, on_delete=models.SET_NULL)



