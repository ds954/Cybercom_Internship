from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username=models.CharField(max_length=100)
    firstname=models.CharField(max_length=100)
    lastname=models.CharField(max_length=100)
    email=models.EmailField()

    def __str__(self):
        return self.firstname
