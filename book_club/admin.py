from django.contrib import admin
from posts.models import Post


class PostAdmin(admin.ModelAdmin):
    pass  # This just tells Django to use the default settings.

    admin.site.register(Post, PostAdmin)
