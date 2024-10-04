from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

