from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from utils.admin import BaseAdmin, admin
from .models import CustomUser as User


@admin.register(User)
class UserAdmin(BaseUserAdmin, BaseAdmin):
    def get_fieldsets_dict(self, request, obj=None):
        default_fieldsets_dict = super().get_fieldsets_dict(request, obj)
        default_fieldsets_dict.update(
            {
                self.lookup_general_key: {
                    "label": self.fieldsets[0][0],
                    "value": self.fieldsets[0][1],
                },
                "personal-info": {
                    "label": self.fieldsets[1][0],
                    "value": self.fieldsets[1][1],
                },
                "permissions": {
                    "label": self.fieldsets[2][0],
                    "value": self.fieldsets[2][1],
                },
            }
        )
        for i in self.fieldsets[3][1]["fields"]:
            default_fieldsets_dict[self.lookup_important_dated_key]["value"]["fields"].insert(0, i)
        self.lookup_key_list = [self.lookup_general_key, "personal-info", "permissions",
                                self.lookup_important_dated_key]
        return default_fieldsets_dict
