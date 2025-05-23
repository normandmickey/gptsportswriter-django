from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import base64

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
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
    
    def get_image_bytes(self):
        return base64.b64encode(self.gameimg).decode('utf-8')

    
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
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
    
    def get_image_bytes(self):
        return base64.b64encode(self.gameimg).decode('utf-8')
 

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
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
    
    def get_image_bytes(self):
        return base64.b64encode(self.gameimg).decode('utf-8')
 

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
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
    
    def get_image_bytes(self):
        return base64.b64encode(self.gameimg).decode('utf-8')
    
