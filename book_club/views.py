from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from .models import Book
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout


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


class ManageView(View):
    def get(self, request):
        return render(request, 'manage.html')

    def post(self, request):
        title = request.POST.get('title')
        book_title = request.POST.get('book_title')
        book_author = request.POST.get('book_author')
        book_description = request.POST.get('book_description')

        # Create a new Book instance
        book = Book.objects.create(
            title=title,
            book_title=book_title,
            book_author=book_author,
            book_description=book_description
        )

        return redirect('index')  # Redirect to the index page after creating the book


def book_c(request):
    page_title = "Book club"
    return render(request, 'book.html', {'page_title': page_title})
