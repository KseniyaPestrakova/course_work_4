from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email", help_text="Укажите email")
    fio = models.CharField(max_length=150, verbose_name="ФИО", help_text="Укажите свои фамилию, имя и отчество")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["fio"]


class Message(models.Model):
    subject = models.CharField(max_length=350, verbose_name="Тема письма")
    body = models.TextField(blank=True, null=True, help_text="Введите текст сообщения")

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Newsletter(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('Completed', 'Завершена'),
    ]

    start_sent_at = models.DateTimeField(verbose_name='Дата и время первой отправки')
    finish_sent_at = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='Статус рассылки'
    )
    message = models.ForeignKey(Message, blank=True, null=True, on_delete=models.SET_NULL)
    subscribers = models.ManyToManyField(Subscriber, related_name='newsletter_subscribers')

    def __str__(self):
        return f' Рассылка id {self.pk}'

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"



