import smtplib

from django.core.mail import BadHeaderError, send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER

from .models import AttemptSent, Newsletter


def sent_newsletter(newsletter):
    subscribers = newsletter.subscribers.all()
    for subscriber in subscribers:
        try:
            send_mail(
                subject=newsletter.message.subject,
                message=newsletter.message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[subscriber.email],
            )

            AttemptSent.objects.create(
                newsletter=newsletter,
                created_at=timezone.now(),
                status=AttemptSent.SUCCESSFUL,
                server_response="Письмо успешно отправлено",
                owner=newsletter.owner,
            )
        except (smtplib.SMTPException, BadHeaderError) as e:
            AttemptSent.objects.create(
                newsletter=newsletter,
                created_at=timezone.now(),
                status=AttemptSent.NOT_SUCCESSFUL,
                server_response=str(e),
                owner=newsletter.owner,
            )


def run_newsletter(newsletter_id):
    try:
        newsletter = Newsletter.objects.get(id=newsletter_id)
        # Обновляем статус рассылки на "Запущена"
        newsletter.status = Newsletter.LAUNCHED
        newsletter.start_sent_at = timezone.now()
        newsletter.save()

        # Инициализируем отправку писем
        sent_newsletter(newsletter)

        # После завершения обновляем статус на "Завершена"
        newsletter.finish_sent_at = timezone.now()
        newsletter.status = Newsletter.COMPLETED
        newsletter.save()

    except Newsletter.DoesNotExist:
        print(f"Рассылка с id {newsletter_id} не найдена")
