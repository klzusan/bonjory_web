from django.conf import settings
from django.db import models
from django.utils import timezone

class verPost(models.Model):
    ver_num = models.FloatField()
    ver_text = models.TextField()
    published_date = models.DateTimeField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return f"v{self.ver_num}"