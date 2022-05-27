from django.template.loader import render_to_string
from django.utils.html import strip_tags

from shared.tasks import send_task_mail


def send_email(email, subject, template, context=None):
    """Send email to user using templates"""

    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)

    if isinstance(email, str):
        email = [email]

    send_task_mail(subject, html_message, plain_message, email)

