from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from education.forms import CustomUserCreationForm, CustomUserChangeForm
from education.models import KCBMSUser,Ward,WardAllocation,FinancialYear

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = KCBMSUser
    list_display = ["email", "username",'is_ward_admin','is_edu_admin','is_accountant']

admin.site.register(KCBMSUser, CustomUserAdmin)
admin.site.register(Ward)
admin.site.register(WardAllocation)
admin.site.register(FinancialYear)