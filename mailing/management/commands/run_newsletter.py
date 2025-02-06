from django.core.management import call_command
from django.core.management.base import BaseCommand

from mailing.models import Newsletter
from mailing.services import run_newsletter


class Command(BaseCommand):
    help = "Отправка рассылки по ее ID"

    def add_arguments(self, parser):
        parser.add_argument('newsletter_id', type=int, help='ID рассылки')

    def handle(self, *args, **kwargs):
        newsletter_id = kwargs['newsletter_id']

        try:
            run_newsletter(newsletter_id)
            self.stdout.write(self.style.SUCCESS(f'Рассылка с id {newsletter_id} успешно отправлена'))
        except Newsletter.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Рассылка с id {newsletter_id} не найдена'))
