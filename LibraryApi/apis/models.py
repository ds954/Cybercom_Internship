from django.db import models
class apimodel(models.Model):
    username=models.CharField(max_length=200,blank=True)
    name=models.CharField(max_length=200,default='dhara')
    email=models.EmailField(default='dsm952004@gmail.com')
    password=models.CharField(max_length=200)
    title=models.CharField(max_length=200)
    description=models.TextField()

    def __str__(self):
        return self.title