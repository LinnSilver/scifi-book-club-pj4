from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
    permission_required
)
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Book, Comment
from .forms import BookForm, CommentForm


def index(request):
    """
    View function for the index page.
    """
    page_title = "Sci fi Book Club"
    books = Book.objects.order_by('-created_on')
    latest_book = Book.objects.order_by('-id').first()
    return render(request, 'index.html', {
        'books': books,
        'latest_book': latest_book,
        'page_title': page_title})


def is_superuser(user):
    """
    Check if a user has the Superuser status.
    """
    return user.is_superuser


#####
# Log in, out and sign up
#####

def signup(request):
    """
    Sign up page.
    """
    page_title = "Sign up"
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
            messages.error(request, 'Error creating the account.'
                                    ' Please check the form and try again.')

    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {
        'form': form,
        'page_title': page_title
    })


class UserLoginView(LoginView):
    """
    Custom login view class.
    """
    template_name = 'login.html'
    success_url = reverse_lazy('index')
    authentication_form = AuthenticationForm
    page_title = 'Login'

    def get_context_data(self, **kwargs):
        """
        Get additional context data for the template.
        """
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

    def form_valid(self, form):
        """
        Handle the case when the login form is valid.
        """
        user = form.get_user()
        login(self.request, user)
        messages.success(self.request, 'You are logged in!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid login credentials.')
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in!')
            return super().form_valid(self.get_form())
        else:
            messages.error(request, 'Invalid login credentials.')
            return super().form_invalid(self.get_form())


def logout_view(request):
    """
    View function to handle user logout.
    """
    logout(request)
    messages.success(request, 'You are logged out!')
    return redirect('index')


#####
# Books
#####

@login_required
@permission_required('app_name.permission_name', login_url='/login/')
def manager(request):
    """
    View function for the book manager page.
    """
    page_title = "Manage book"
    books = Book.objects.order_by('-created_on')
    form = BookForm()

    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('manager')

    return render(request, 'manager.html', {
        'page_title': page_title,
        'books': books,
        'form': form
    })


@login_required
@user_passes_test(is_superuser, login_url='/login/')
class ManagerView(View):
    """
    View function to update a book.
    """
    def get(self, request):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, 'You need to be logged in as a '
                                    'librarian to access this page.')

            return redirect('login')

        form = BookForm()
        return render(request, 'manager.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST)

        if form.is_valid():
            book = form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('book_detail')
        else:
            messages.error(
                request, 'Error creating book. Please check the form.'
            )

        return render(request, 'manager.html', {'form': form})


@login_required
@user_passes_test(is_superuser, login_url='/login/')
def update_book(request, book_id):
    """
    View function to update a book.
    """
    page_title = "Update book"
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('manager')
    else:
        form = BookForm(instance=book)

    return render(request, 'update_book.html', {
        'form': form,
        'book': book,
        'page_title': page_title
    })


def book_detail(request, book_id):
    """
    View function for the book detail page.
    """
    page_title = "Book club"
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(book=book)
    page_title = book.title
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('book_detail', book_id=book_id)

    return render(request, 'book_detail.html', {
        'book': book,
        'comments': comments,
        'form': form,
        'page_title': page_title
    })


@login_required
@user_passes_test(is_superuser, login_url='/login/')
def delete_book(request, book_id):
    """
    Function to delete a book.
    """
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    messages.success(request, 'Book deleted!')
    return redirect('index')


#####
# Comments
#####

@login_required
def add_comment(request, book_id):
    """
    View function to add a comment to a book.
    """
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book_id = book_id
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment created!')
            return redirect('book_detail', book_id=book_id)
    else:
        form = CommentForm()

    return redirect('book_detail', book_id=book_id)


@login_required
def delete_comment(request, comment_id):
    """
    Function to delete a comment.
    """
    comment = get_object_or_404(Comment, id=comment_id)

    # Check if the logged-in user is the owner of the comment
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted!')
        return redirect('book_detail', book_id=comment.book.id)

    return redirect('book_detail', book_id=comment.book.id)


#####
# Errors
#####

def page_not_found(request, exception):
    return render(request, 'errors/404.html', status=404)


def server_error(request):
    return render(request, '500.html', status=500)


def permission_denied(request, exception):
    return render(request, '403.html', status=403)


def method_not_allowed(request, exception):
    return render(request, '405.html', status=405)
