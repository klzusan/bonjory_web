from django.contrib import admin
from .models import verPost, serialNumber, zipFile, CustomUser

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

# Register your models here.
admin.site.register(verPost)

@admin.register(serialNumber)
class serialNumberAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'get_user_email', 'created_at')

    def get_user_email(self, obj):
        return obj.user.email if obj.user else '未登録'
    get_user_email.short_description = 'Email'

@admin.register(zipFile)
class zipFileAdmin(admin.ModelAdmin):
    list_display = ('upload', 'upload_at')

# Custom user
class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'is_active', 'is_staff', 'is_superuser')

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email',)

class CustomUserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'is_staff', 'is_active', 'is_superuser')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Date Info', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password2'),
        }),
    )

    list_filter = ('is_staff', 'is_superuser', 'is_active')

    search_fields = ('email',)

    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
# End of CustomUser