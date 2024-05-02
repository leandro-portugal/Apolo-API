from django.db import models 
from django.contrib.auth.models import AbstractBaseUser, Permission

class User(AbstractBaseUser):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_owner = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    def __str__(self) -> str:
        return self.email
    
class Group(models.Model):
    name = models.CharField(max_length=96)
    enterprise = models.ForeignKey('companies.Enterprise', on_delete=models.CASCADE)

class GroupPermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

class UserGroups(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
