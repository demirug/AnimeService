from django.core import mail

from app import settings
from app.celery import app


@app.task(bind=True, default_retry_delay=10)
def send_task_mail(self, subject, html_message, plain_message, recipient):
    try:
        mail.send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, recipient, html_message=html_message)
    except Exception as exc:
        raise self.retry(exc=exc)
