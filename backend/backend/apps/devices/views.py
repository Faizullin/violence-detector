from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView
from rest_framework_api_key.models import APIKey

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
    fields = ['name', 'description']
    success_url = reverse_lazy('devices:device-list-my')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    template_name = 'devices/device_edit.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('devices:device-list-my')

    def get_queryset(self):
        # Ensure the user can only update their own devices
        return Device.objects.filter(user=self.request.user)


class APIKeyRegenerateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Delete the old API key
        APIKey.objects.filter().delete()
        # Create a new API key
        APIKey.objects.create_key(name=f"user-{request.user.id}")
        return HttpResponseRedirect(reverse('device_detail', args=[kwargs['pk']]))
