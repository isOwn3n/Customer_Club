from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    exclude = ("deleted_at", )

# admin.site.register(models.Customer)
admin.site.register(models.Group)
