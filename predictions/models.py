from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import base64
import random
import string

def generate_random_string(length=4):
    """Generates a random string of given length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_unique_slug(instance, slug_field, title, new_slug=None):
    """Generates a unique slug for a given instance."""
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(title)

    Klass = instance.__class__
    if Klass.objects.filter(**{slug_field: slug}).exists():
        new_slug = f"{slug}-{generate_random_string()}"
        return generate_unique_slug(instance, slug_field, title, new_slug=new_slug)
    return slug

class Predictions(models.Model):
    id = models.TextField(primary_key=True)
    content = models.TextField()
    gameimg = models.BinaryField()
    title = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=False, max_length=255)
    sport_key=models.TextField(default="baseball_mlb")
    tweet_text=models.TextField(blank=True)
    won=models.BooleanField(null=True)
    results=models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            #self.slug = slugify(self.title)
            self.slug = generate_unique_slug(self, 'slug', self.title)
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
    sport_key=models.TextField(default="baseball_mlb")
    tweet_text=models.TextField(blank=True)
    won=models.BooleanField(null=True)
    results=models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            #self.slug = slugify(self.title)
            self.slug = generate_unique_slug(self, 'slug', self.title)
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
    sport_key=models.TextField(default="baseball_mlb")
    tweet_text=models.TextField(blank=True)
    won=models.BooleanField(null=True)
    results=models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            #self.slug = slugify(self.title)
            self.slug = generate_unique_slug(self, 'slug', self.title)
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
    sport_key=models.TextField(default="baseball_mlb")
    tweet_text=models.TextField(blank=True)
    won=models.BooleanField(null=True)
    results=models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            #self.slug = slugify(self.title)
            self.slug = generate_unique_slug(self, 'slug', self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"slug": self.slug})
    
    def get_image_bytes(self):
        return base64.b64encode(self.gameimg).decode('utf-8')
    
