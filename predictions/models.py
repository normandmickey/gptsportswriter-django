from django.db import models
from django.utils import timezone

class Predictions(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Recaps(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Parlays(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

class Props(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    