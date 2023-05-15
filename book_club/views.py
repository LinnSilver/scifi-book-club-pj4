from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Book
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.shortcuts import render, redirect


def index(request):
    page_title = "Sci fi Book Club"
    return render(request, 'index.html', {'page_title': page_title})


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


class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page or do something else
            return super().form_valid(form)  # If you want to redirect to the success_url
        else:
            # Return an invalid login error message or redirect back to the login page with an error message
            return super().form_invalid(form)  # If you want to redirect back to the login page


def signup(request):
    page_title = "Signup"
    form = SignUpForm()

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirect to the desired page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'page_title': page_title}, {'form': form})


def manager(request):
    page_title = "Manage book"
    return render(request, 'manager.html', {'page_title': page_title})


def book(request):
    page_title = "Book club"
    return render(request, 'book.html', {'page_title': page_title})
