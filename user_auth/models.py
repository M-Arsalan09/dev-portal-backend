from django.db import models

# Create your models here.

class UserAuth(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    first_login = models.BooleanField(default=True)
    role = models.CharField(max_length=200, default="developer")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email