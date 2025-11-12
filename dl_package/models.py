from django.conf import settings
from django.db import models
from django.utils import timezone
from .validators import validate_is_zip
import os
from .storages import OverwriteStorage
from django.contrib.auth.models import User

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
    description = models.CharField(max_length = 255, blank=True)
    upload = models.FileField(
        upload_to=zip_upload_path,
        validators=[validate_is_zip],
        storage=OverwriteStorage()
        )
    upload_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description or str(self.upload)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class serialNumber(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    serial_number = models.CharField(max_length=8, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.serial_number}"