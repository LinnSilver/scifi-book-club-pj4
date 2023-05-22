from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book, Comment


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ('content',)

    def save(self, commit=True, **kwargs):
        comment = super().save(commit=False)
        if 'user' in kwargs:
            comment.user = kwargs['user']
        if commit:
            comment.save()
        return comment


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'book_title', 'book_author', 'book_description']
