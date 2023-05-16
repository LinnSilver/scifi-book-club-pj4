from django.urls import path
from . import views
from .views import logout_view


urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('logout/', logout_view, name='logout'),
]
