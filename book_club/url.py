from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailsView.as_view(), name='book_details'),
]