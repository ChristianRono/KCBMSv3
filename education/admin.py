from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from education.forms import CustomUserCreationForm, CustomUserChangeForm
from education.models import KCBMSUser,Ward,WardAllocation,FinancialYear


fields = list(UserAdmin.fieldsets)
fields[-2] = (
            'User Type',
            {
                'fields':(
                    'is_ward_admin',
                    'is_edu_admin',
                    'is_accountant',
                ),
            }
        )

UserAdmin.fieldsets = tuple(fields)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = KCBMSUser

    

admin.site.register(KCBMSUser, CustomUserAdmin)
admin.site.register(Ward)
admin.site.register(WardAllocation)
admin.site.register(FinancialYear)