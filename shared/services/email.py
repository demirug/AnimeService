from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail


def send_email(email, subject, template, context=None):
    """Send email to user using templates"""
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)
    mail.send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [email], html_message=html_message,
                   fail_silently=True)
    #TODO send email by celery task
