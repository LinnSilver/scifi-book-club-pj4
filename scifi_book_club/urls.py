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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from book_club import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('manager/', views.manager, name='manager'),
    path('manage/', views.ManageView.as_view(), name='manage'),
    path('book_club/', views.book_c, name='book_club'),
]

"""
from django.contrib.auth import views as auth_views
from book_club.views import signup, index, UserLoginView

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('book_club/', include('book_club.urls')),
    path('my-view/', views.my_view, name='my_view'),
    path('', index, name='index'),
    path('logout/', logout_view, name='logout'),
    path('manager/', manager, name='manager'),
    path('manage/', ManageView.as_view(), name='manage'),
"""