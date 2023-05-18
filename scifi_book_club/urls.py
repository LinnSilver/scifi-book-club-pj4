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
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from book_club import views
from django.contrib.auth import get_user_model
from book_club.views import add_comment
from book_club.views import delete_comment


User = get_user_model()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('manager/', views.manager, name='manager'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book/update/<int:book_id>/', views.update_book, name='update_book'),
    path('book/delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('add_comment/<int:book_id>/', add_comment, name='add_comment'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),

]
