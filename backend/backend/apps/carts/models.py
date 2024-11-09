# from django.contrib.auth import get_user_model
# from django.utils.translation import gettext_lazy as _
#
# from apps.products.models import Product
# from utils.models import AbstractTimestampedModel, models
#
# UserModel = get_user_model()
#
#
# class CartItem(AbstractTimestampedModel):
#     user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
#     quantity = models.FloatField(_("Quantity"), default=1)
#
#     def add_amount(self):
#         amount = self.product.price * self.quantity
#         profile = self.user.profile
#         profile.total_price = profile.total_price + amount
#         profile.save()
#         return True
#
#     def __str__(self):
#         return self.product.name
