from django.db import models

class Quotes(models.Model):
    name = models.TextField()
    source = models.CharField(max_length=50)
    weight = models.PositiveIntegerField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)
