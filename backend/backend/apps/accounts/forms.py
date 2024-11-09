from dj_rest_auth.forms import AllAuthPasswordResetForm as _BaseAllAuthPasswordResetForm, default_url_generator

from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm as _BasePasswordResetForm
from django.contrib.sites.shortcuts import get_current_site

if 'allauth' in settings.INSTALLED_APPS:
    from allauth.account import app_settings as allauth_account_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.forms import default_token_generator
    from allauth.account.utils import (
        user_pk_to_url_str,
        user_username,
    )

from utils.send_email_message_tasks import send_email_message


class AllAuthPasswordResetForm(_BaseAllAuthPasswordResetForm):
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)

            # save it to the password reset model
            # password_reset = PasswordReset(user=user, temp_key=temp_key)
            # password_reset.save()

            # send the password reset email
            url_generator = kwargs.get('url_generator', default_url_generator)
            url = url_generator(request, user, temp_key)
            uid = user_pk_to_url_str(user)

            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
                'token': temp_key,
                'uid': uid,
            }
            if (
                    allauth_account_settings.AUTHENTICATION_METHOD != allauth_account_settings.AuthenticationMethod.EMAIL
            ):
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'account/email/password_reset_key', email, context
            )
        return self.cleaned_data['email']


class PasswordResetForm(_BasePasswordResetForm):
    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()
