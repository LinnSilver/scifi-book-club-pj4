from django.urls import path
from . import views
from .views import logout_view
from .views import ManageView
from .views import manager

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('manage/', ManageView.as_view(), name='manage'),
    path('manager/', manager, name='manager'),
]
