from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Book


class BookDetailsView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        comments = post.comments.filter(approved=True).order_by("-created_on")
        liked = False
    if post.likes.filter(id=self.request.user.id).exists():
        liked = True

    return render(request, 'book_detail.html', {'book': book})
