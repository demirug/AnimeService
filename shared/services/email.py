from django.template.loader import render_to_string
from django.utils.html import strip_tags

from shared.tasks import send_task_mail


def send_email(emails, subject, html_message):
    """Send to user html email"""
    if isinstance(emails, str):
        emails = [emails]
    print(html_message)
    #for email in emails:
    #    send_task_mail.delay(subject, html_message, strip_tags(html_message), [email])


def send_template_email(emails, subject, template, context=None):
    """Send email to user using templates"""

    html_message = render_to_string(template, context)
    send_email(emails, subject, html_message)