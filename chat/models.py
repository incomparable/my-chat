from django.conf import settings
from django.db import models
from django.utils import timezone


class Message(models.Model):
    creator = models.CharField(max_length=500)
    receiver = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=500)
    
    def publish(self):
        self.published_date = timezone.now()
        self.save()
        

    def __str__(self):
        return self.title