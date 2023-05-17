from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        # widgets = {
        #    'info': forms.Textarea(attrs={'placeholder': 'Comment'}),
        # }


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'book_title', 'book_author', 'book_description']
