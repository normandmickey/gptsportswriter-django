from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Predictions(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=False, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    
class Recaps(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=False, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
 

class Parlays(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=False, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
 

class Props(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=False, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
