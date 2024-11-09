from allauth.account.adapter import *
from django.conf import settings
from django.http import HttpResponseRedirect

from utils.send_email_message_tasks import send_email_message


class AccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, email_confirmation, signup):
        return super().send_confirmation_mail(request, email_confirmation, signup)

    def send_mail(self, template_prefix, email, context):
        ctx = {
            "email": email,
            "current_site": get_current_site(globals()["context"].request),
        }
        ctx.update(context)
        send_email_message(context=context, user_emails=[email])

    def get_email_confirmation_url(self, request, email_confirmation):
        url = settings.FRONTEND_APP_BASE_URL + f"/auth/verify-email/{email_confirmation.key}/"
        return url

    def respond_email_verification_sent(self, request, email_confirmation):
        url = settings.FRONTEND_APP_BASE_URL
        return HttpResponseRedirect(url)
