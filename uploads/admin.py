from django.contrib import admin
from .models import Upload


class UploadAdmin(admin.ModelAdmin):
    list_display = ["model_name", "created_at"]


# Register your models here.
admin.site.register(Upload, UploadAdmin)
