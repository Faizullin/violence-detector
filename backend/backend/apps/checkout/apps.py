from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'apps.checkout'

    def ready(self):
        import apps.checkout.signals
