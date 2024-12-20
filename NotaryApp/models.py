from django.db import models
from django.contrib.auth.models import User
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import base64

class NotaryDocument(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    document_hash = models.CharField(max_length=64)
    pin = models.CharField(max_length=6, null=True, blank=True)
    details = models.TextField(default='')
    transaction_hash = models.CharField(max_length=66, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    public_key = models.TextField(null=True, blank=True)
    private_key = models.TextField(null=True, blank=True)  # Store encrypted

    def generate_key_pair(self):
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        
        # Get public key
        public_key = private_key.public_key()
        
        # Serialize private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize public key
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        # Store as base64 strings
        self.private_key = base64.b64encode(private_pem).decode('utf-8')
        self.public_key = base64.b64encode(public_pem).decode('utf-8')

    def __str__(self):
        return f"{self.filename} - {self.user.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    eth_address = models.CharField(max_length=42, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    eid_number = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return self.user.username