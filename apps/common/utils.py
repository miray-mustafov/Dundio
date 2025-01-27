from django.http import HttpResponseBadRequest
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
import uuid

from apps.users.models import UserConfirmationToken


def send_confirmation_email(user, request, template_name):
    """
    Creates uuid based token and saves it to db
    Renders proper html with the corresponding context
    Sends email message to the recipient
    """
    token = str(uuid.uuid4())
    base_url = request.scheme + '://' + request.get_host()
    UserConfirmationToken.objects.create(user=user, token=token)

    subject = _('Линк за потвърждение')
    sender = settings.EMAIL_HOST_USER

    html_content = render_to_string(
        template_name,
        context={
            "token": token,
            "recipient_email": user.email,
            "base_url": base_url,
        },
    )

    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=sender,
        to=[user.email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def request_is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'
