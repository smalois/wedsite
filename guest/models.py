from django.db import models
from django.contrib.auth.models import User

class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hasVoted = models.BooleanField()
    scavProgress = models.CharField(max_length=16, default='0000000000000000')