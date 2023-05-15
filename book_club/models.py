from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    author = models.CharField(max_length=100)
    description = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_books', blank=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    slug = models.SlugField(max_length=50, unique=True, default='')
    status = models.CharField(max_length=10, choices=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    ),  null=True)
    created_on = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug from the title if it's not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.SlugField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    ))
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
