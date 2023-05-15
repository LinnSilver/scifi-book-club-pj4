from django.contrib import admin
from book_club.models import Post
from django.contrib.auth.models import User, Group, Permission
from .models import Book


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}


# Creates an inline class for managing user permissions:
class PermissionInline(admin.TabularInline):
    model = User.user_permissions.through
    extra = 1


# Create an inline class for managing user groups:
class GroupInline(admin.TabularInline):
    model = User.groups.through
    extra = 1


# Unregister the default UserAdmin class
admin.site.unregister(User)


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [PermissionInline, GroupInline]


# Register Permission models with the admin site:
admin.site.register(Permission)


admin.site.register(Book)