from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Book
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from book_club import views
from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect


def index(request):
    page_title = "Sci fi Book Club"
    return render(request, 'index.html', {'page_title': page_title})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    authentication_form = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Redirect to a success page or do something else
            return super().form_valid(self.get_form())  # If you want to redirect to the success_url
        else:
            # Return an invalid login error message or redirect back to the login page with an error message
            return super().form_invalid(self.get_form())  # If you want to redirect back to the login page


def logout_view(request):
    logout(request)
    return redirect('index')


def manager(request):
    page_title = "Manage book"
    return render(request, 'manager.html', {'page_title': page_title})


def book(request):
    page_title = "Book club"
    return render(request, 'book.html', {'page_title': page_title})


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