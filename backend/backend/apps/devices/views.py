from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView
from rest_framework_api_key.models import APIKey
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.accounts.permissions import permissions

from .forms import DeviceForm
from .models import Device


class DeviceListView(LoginRequiredMixin, ListView):
    model = Device
    template_name = 'devices/device_list.html'
    context_object_name = 'devices'

    def get_queryset(self):
        return Device.objects.filter(user=self.request.user)


class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    template_name = 'devices/device_create.html'
    success_url = reverse_lazy('devices:device-list-my')
    form_class = DeviceForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    template_name = 'devices/device_edit.html'
    success_url = reverse_lazy('devices:device-list-my')
    form_class = DeviceForm

    def get_queryset(self):
        # Ensure the user can only update their own devices
        return Device.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context.update({ "device": self.object })
        return context


class APIKeyRegenerateView(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    def post(self, request, id, *args, **kwargs):
        # # Delete the old API key
        # APIKey.objects.filter().delete()
        # # Create a new API key
        _, key_str = APIKey.objects.create_key(name=f"user-{request.user.id}")
        return Response({"data": {
            "hashed_key": key_str,
        } })
