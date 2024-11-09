from dj_rest_auth.serializers import JWTSerializerWithExpiration as _BaseJWTSerializerWithExpiration
from dj_rest_auth.serializers import PasswordResetSerializer as _BasePasswordResetSerializer

from utils.serializers import get_datetime_formatted, serializers, TimestampedSerializer
from .models import UserProfile


class JWTSerializerWithExpiration(_BaseJWTSerializerWithExpiration):
    """
    Serializer for JWT authentication with expiration times.
    """
    access_expiration = serializers.SerializerMethodField(read_only=True)
    refresh_expiration = serializers.SerializerMethodField(read_only=True)

    def get_access_expiration(self, obj):
        return get_datetime_formatted(obj['access_expiration'])

    def get_refresh_expiration(self, obj):
        return get_datetime_formatted(obj['refresh_expiration'])


class PasswordResetSerializer(_BasePasswordResetSerializer):
    pass
    # def get_email_options(self):
    #     return {
    #         'subject_template_name': 'registration/password_reset_subject.txt',
    #         'email_template_name': 'registration/password_reset_message.txt',
    #         'html_email_template_name': 'registration/'
    #                                     'password_reset_message.html',
    #         'extra_email_context': {
    #             'pass_reset_obj': self.your_extra_reset_obj
    #         }
    #     }
    # def save(self):
    #     request = self.context.get('request')
    #     opts = {
    #         'use_https': request.is_secure(),
    #         'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
    #
    #         ###### USE YOUR TEXT FILE ######
    #         'email_template_name': 'example_message.txt',
    #
    #         'request': request,
    #     }
    #     self.reset_form.save(**opts)


class UserProfileSerializer(TimestampedSerializer):
    class Meta:
        model = UserProfile
        fields = ['default_email', 'default_address_line_1', 'default_address_line_2',
                  'default_town_or_city', 'default_county', 'default_postcode', 'default_is_gift_wrapping',
                  'created_at', 'updated_at', ]
