from django.db import models

# Create your models here.
class Comment(models.Model):
    comment_text=models.TextField()

    def __str__(self):
        return self.comment_text
    