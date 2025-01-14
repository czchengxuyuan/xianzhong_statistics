from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    
    is_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # 电话号码
    address = models.TextField(blank=True, null=True)  # 地址

    def __str__(self):
        return self.username
    
    def is_custom_admin(self):
        return self.is_admin and self.is_staff