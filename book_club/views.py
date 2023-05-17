from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from .models import Book
from django.contrib.auth.decorators import user_passes_test
from .forms import BookForm


def index(request):
    page_title = "Sci fi Book Club"
    books = Book.objects.all()
    latest_book = Book.objects.order_by('-id').first()
    return render(request, 'index.html', {'books': books, 'latest_book': latest_book})


def book_detail(request, book_id):
    page_title = "Book club"
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'book_detail.html', {'book': book, 'page_title': page_title})


def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('manager')
    else:
        form = BookForm(instance=book)

    return render(request, 'update_book.html', {'form': form, 'book': book})


def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return redirect('index')


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
            # Return an success message and redirect page to success_url
            return super().form_valid(self.get_form())  # Redirect to the success_url
        else:
            # Return an invalid login error message and redirect back to the login page with an error message
            return super().form_invalid(self.get_form())  # Redirect back to the login page


def logout_view(request):
    logout(request)
    return redirect('index')


@permission_required('app_name.permission_name', login_url='/login/')
def manager(request):
    page_title = "Manage book"
    books = Book.objects.order_by('created_on')  # Retrieve all books from the database
    form = BookForm()  # Create an instance of the BookForm

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manager')

    return render(request, 'manager.html', {'page_title': page_title, 'books': books, 'form': form})


# checks whether a user has the Superuser status
def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser, login_url='/login/')
class ManagerView(View):
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, 'You need to be logged in as a librarian to access this page.')
            return redirect('login')
        return render(request, 'manager.html')

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


def page_not_found(request, exception):
    return render(request, 'errors/404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)


def permission_denied(request, exception):
    return render(request, '403.html', status=403)


def method_not_allowed(request, exception):
    return render(request, '405.html', status=405)