from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class Books(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    total_quantity = models.BigIntegerField()
    aval_quantity = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Author: {self.author}, Book Title: {self.title}, Genre: {self.genre}, Date Published: {self.date}, have { self.total_quantity} in stock"
