from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Book


def home(request):
    return render(request, 'index.html')


class BookDetailsView(View):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        comments = book.comments.filter(approved=True).order_by("-created_on")
        liked = False
        if book.likes.filter(id=request.user.id).exists():
            liked = True

        return render(request, 'book_detail.html', {'book': book})


class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'book_list.html', {'books': books})
