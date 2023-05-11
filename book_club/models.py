from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    content = models.TextField()
    slug = models.SlugField(max_length=50, unique=True, default='')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug from the title if it's not provided
        super().save(*args, **kwargs)

    status = models.CharField(max_length=10, choices=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    ))
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
