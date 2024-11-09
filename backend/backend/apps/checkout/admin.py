from django.contrib import admin

from utils.admin import BaseAdmin
from .models import Order, OrderLineItem, Payment


class OrderLineItemAdminInline(admin.TabularInline):
    # """
    # This inline item is going to allow us to add and edit line
    # items in the admin right from inside the order model.
    # """
    #
    # has_default_timestamps = False
    # has_soft_delete = False
    #
    # def __init__(self, model, admin_site):
    #     super(OrderLineItemAdminInline, self).__init__(model, admin_site)
    #     self.has_default_timestamps = self.check_has_default_timestamps()
    #     self.has_soft_delete = self.check_has_soft_delete()
    #     if self.has_default_timestamps:
    #         self.readonly_fields += ("created_at", "updated_at",)
    #     if self.has_soft_delete:
    #         self.readonly_fields += ("deleted_at",)
    #
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)
    #
    # def get_fields(self, request, obj=None):
    #     default = super().get_fields(request, obj)
    #     if self.has_default_timestamps:
    #         default.remove('is_deleted')
    #     if obj is None:
    #         if self.has_default_timestamps:
    #             default.remove('deleted_at')
    #     else:
    #         if not self.has_default_timestamps:
    #             default.remove('deleted_at')
    #     return default
    #
    # def check_has_default_timestamps(self):
    #     field_name_list = [field.name for field in self.model._meta.get_fields()]
    #     return 'created_at' in field_name_list and 'updated_at' in field_name_list
    #
    # def check_has_soft_delete(self):
    #     field_name_list = [field.name for field in self.model._meta.get_fields()]
    #     return 'deleted_at' in field_name_list and 'is_deleted' in field_name_list
    #
    # def get_queryset(self, request):
    #     return self.model.all_objects.all()
    #
    # def delete_queryset(self, request, queryset):
    #     if self.has_soft_delete:
    #         soft_delete_queryset(queryset)
    #     else:
    #         hard_delete_queryset(queryset)
    #
    # def delete_model(self, request, obj):
    #     if self.has_soft_delete:
    #         soft_delete_queryset(obj)
    #     else:
    #         hard_delete_queryset(obj)


@admin.register(Order)
class OrderAdmin(BaseAdmin):
    inlines = (OrderLineItemAdminInline,)
    readonly_fields = ('order_number',
                       'delivery_cost', 'order_total',
                       'grand_total', 'original_cart', 'stripe_pid')

    fields = ('order_number', 'user', 'first_name',
              'last_name', 'email', 'address_line_1', 'address_line_2',
              'postcode', 'town_or_city', 'county', 'delivery_cost',
              'order_total', 'grand_total', 'original_cart', 'stripe_pid')

    list_display = ('order_number', 'first_name',
                    'last_name', 'order_total', 'delivery_cost',
                    'grand_total',)


@admin.register(Payment)
class PaymentAdmin(BaseAdmin):
    raw_id_fields = ('user',)
    exclude = ['is_deleted']
