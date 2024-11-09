from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = get_task_logger(__name__)


class SiteUrls:
    RESET_PASSWORD_CONFIRM_URL = settings.FRONTEND_APP_BASE_URL + \
                                 "/auth/password-reset/confirm"
    PROFILE_URL = settings.FRONTEND_APP_BASE_URL + "/dashboard/profile"
    DASHBOARD_URL = settings.FRONTEND_APP_BASE_URL + "/dashboard/"
    SITE_COMMAND = settings.SITE_COMMAND
    SITE_URL = settings.FRONTEND_APP_BASE_URL


def send_email_message(context: dict, user_emails: list):
    send_email_message_task.delay(context, user_emails)


@shared_task
def send_email_message_task(context: dict, user_emails: list):
    logger.info(f"Email: context {context}")
    try:
        context.update({
            'profile_url': SiteUrls.PROFILE_URL,
            'dashboard_url': SiteUrls.DASHBOARD_URL,
            'domain_name': SiteUrls.SITE_COMMAND,
        })
        email_html_message = render_to_string(
            context['app.content.html'], context)
        email_plaintext_message = render_to_string(
            context['app.content.txt'], context)

        msg = EmailMultiAlternatives(
            # title:
            context["app.title"] if "app.title" in context else "Notification from {title}".format(
                title=SiteUrls.SITE_COMMAND),
            # message:
            email_plaintext_message,
            # to:
            to=user_emails
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
    except Exception as err:
        logger.error(f"send_email_message Error: {err}")