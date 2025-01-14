from django.db import models

# Create your models here.

class Accident(models.Model):

    address = models.CharField(max_length=200)
    accident_date = models.DateField()
    description = models.TextField()
    accident_type = models.CharField(max_length=200)
    injured = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)
    unknown = models.IntegerField(default=0)
    
    latitude = models.FloatField()
    longitude = models.FloatField()

    video_link = models.CharField(max_length=200)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"事故：{self.address} - {self.accident_date}"