from django.contrib import admin

# Register your models here.
from .models import Company_Info, Credit_Info

admin.site.register(Company_Info)
admin.site.register(Credit_Info)