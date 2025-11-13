from django.contrib import admin
from .models import verPost, serialNumber, zipFile

# Register your models here.
admin.site.register(verPost)

@admin.register(serialNumber)
class serialNumberAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'get_user', 'created_at')

    def get_user(self, obj):
        return obj.user.username if obj.user else '未登録'
    get_user.short_description = 'User'

@admin.register(zipFile)
class zipFileAdmin(admin.ModelAdmin):
    list_display = ('upload', 'upload_at')