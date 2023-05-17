from django.urls import path
from . import views
from .views import logout_view
from .views import ManagerView
from .views import manager
from .views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout_view, name='logout'),
    path('manager/', ManagerView.as_view(), name='manager'),
    path('manager/', manager, name='manager'),
    path('login/', LoginView.as_view(), name='login'),
]
