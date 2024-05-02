from django.db import models
from accounts.models import User

class Enterprise(models.Model):
    name = models.CharField(max_length=192)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
