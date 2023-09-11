from django.contrib import admin
from applicant.models import Profile,Sibling,Application

# Register your models here.
admin.site.register(Profile)
admin.site.register(Sibling)
admin.site.register(Application)