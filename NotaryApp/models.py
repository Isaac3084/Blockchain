from django.db import models
from django.contrib.auth.models import User

class NotaryDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    document_hash = models.CharField(max_length=64)
    pin = models.CharField(max_length=6, null=True, blank=True)
    details = models.TextField(default='')
    transaction_hash = models.CharField(max_length=66, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.filename} - {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eth_address = models.CharField(max_length=42, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    eid_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.user.username