from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.utils import timezone


class Book(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    book_title = models.CharField(max_length=200, null=False, blank=False)  # New field for book title
    book_author = models.CharField(max_length=100, null=False, blank=False)  # New field for book author
    book_description = models.TextField(null=False, blank=False)  # New field for book description
    slug = models.SlugField(max_length=50, unique=True)
    status = models.CharField(max_length=10, choices=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    ))
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug from the title if it's not provided
        super().save(*args, **kwargs)
