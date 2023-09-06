from django.conf import settings
from django.core.mail import send_mail


def send_email(
        *,
        subject: str,
        message: str,
        to_email: list[str]
):
    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=to_email
    )
