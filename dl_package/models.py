from django.conf import settings
from django.db import models
from django.utils import timezone

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