"""scifi_book_club URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from book_club.views import index, BookDetailsView, BookListView, UserLoginView, signup
from book_club.views import BookDetailsView
from book_club import views
from django.contrib.auth.models import User



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('signup/', signup, name='signup'),
    path('signup/', views.signup, name='signup'),  # Update to use the correct view function
    path('login/', UserLoginView.as_view(), name='login'),
    path('book/<int:book_id>/', BookDetailsView.as_view(), name='book_detail'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('', include('book_club.urls')),
]
