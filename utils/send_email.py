from threading import Thread
from typing import Any

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_html_email(
        *,
        subject: str,
        message: str,
        to_email: list[str],
        template_name: str,
        context: dict[str, Any]
):
    html_message = render_to_string(template_name, context)
    thread = Thread(
        target=send_mail,
        kwargs={
            'subject': subject,
            'message': message,
            'from_email': settings.DEFAULT_FROM_EMAIL,
            'recipient_list': to_email,
            'html_message': html_message
        }
    )
    thread.start()
