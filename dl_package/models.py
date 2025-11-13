from django.conf import settings
from django.db import models
from django.utils import timezone
from .validators import validate_is_zip
import os
from django.conf import settings
from .storages import OverwriteStorage
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class verPost(models.Model):
    ver_num = models.FloatField()
    ver_text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(default=timezone.now)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.ver_num)
    
def zip_upload_path(instance, filename):
    # 拡張子を保持する
    ext = os.path.splitext(filename)[1]  # 例: ".zip"
    
    # ファイル名をUUIDで強制的に変更
    new_filename = f"Handlime{ext}"
    
    # 保存先パス（'games/' フォルダ内）
    return os.path.join('games', new_filename)

class zipFile(models.Model):
    upload = models.FileField(
        upload_to=zip_upload_path,
        validators=[validate_is_zip],
        storage=OverwriteStorage()
        )
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.upload)
    
# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username
    
class serialNumber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    serial_number = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_identifier = self.user.email if self.user else '未登録'
        return f"{user_identifier} - {self.serial_number}"
    
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールを設定してください')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta: # 👈 Meta クラスを追加 (または既存のものに追記)
        # Adminで表示される単数形の名前
        verbose_name = 'User' 
        # Adminで表示される複数形の名前（Adminのリスト表示や選択画面のタイトルに使われます）
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email