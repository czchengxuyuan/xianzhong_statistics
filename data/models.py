from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Accident(models.Model):

    address = models.CharField(max_length=200)
    accident_date = models.DateField()
    description = models.TextField()
    accident_type = models.CharField(max_length=200)
    injured = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)
    unknown = models.CharField(max_length=200, default='情况未知')
    
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    video_link = models.CharField(max_length=200)
    is_approved = models.BooleanField(False)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"事故：{self.address} - {self.accident_date}"
    

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()  # 消息内容
    created_at = models.DateTimeField(auto_now_add=True)  # 消息创建时间
    read = models.BooleanField(default=False)  # 消息是否已读

    def __str__(self):
        return f"Message to {self.user.username}: {self.content[:50]}..."