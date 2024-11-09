from django.utils.http import urlencode
from django.conf import settings
import time


class DelayMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Change 0 to desired delay in seconds
        self.delay = getattr(settings, "DEV_REQUEST_DELAY", 0)

    def __call__(self, request):
        if request.path.startswith("/api") and self.delay:
            # Log request details for debugging (optional)
            log_message = f"Delaying request '{request.method} {request.path}' for {self.delay} seconds."
            print(log_message, )
            # time.sleep(self.delay)
        response = self.get_response(request)
        return response
