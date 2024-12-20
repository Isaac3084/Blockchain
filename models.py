from django.db import models
from django.contrib.auth.models import User

class NotaryDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    document_hash = models.CharField(max_length=256)
    filename = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=256)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eth_address = models.CharField(max_length=42)  # Ethereum address
    phone = models.CharField(max_length=15)
    eid_number = models.CharField(max_length=50)  # National eID number
    
    def __str__(self):
        return self.user.username
