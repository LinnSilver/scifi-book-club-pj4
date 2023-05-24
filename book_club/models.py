from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Book(models.Model):
    """
    Model representing a book in the application.
    """
    title = models.CharField(max_length=200, null=False, blank=False)
    book_title = models.CharField(max_length=200, null=False, blank=False)
    book_author = models.CharField(max_length=100, null=False, blank=False)
    book_description = models.TextField(null=False, blank=False)
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
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Book.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Model representing comments on a book.
    """
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return f"{self.user.username} says: {self.content}"
